#![feature(custom_derive, custom_attribute, plugin)]
#![plugin(diesel_codegen)]

#[macro_use]
extern crate diesel;
extern crate merge2d;

pub const DB_URL: &'static str = "postgres://localhost/backblaze2";

pub mod schema;

use diesel::prelude::*; // alot of traits + diesel::result::*
use diesel::pg::PgConnection;
use merge2d::Point;
use std::iter::Peekable;

#[derive(Debug, Queryable)]
pub struct DevMaxParams {
    max_load_cc: Option<i64>,
    max_poh: Option<i64>,
    total: i64,
}

pub struct StepItem {
    key: i64,
    val: Point<i64, i64>,
}

pub struct StepIter<I: Iterator> {
    inner: Peekable<I>,
}

impl<I> StepIter<I>
    where I: Iterator<Item=StepItem>
{
    pub fn new(iter: I) -> StepIter<I> {
        StepIter {
            inner: iter.peekable(),
        }
    }

    pub fn next_step<'a>(&'a mut self) -> Option<(i64, ParamIter<'a, I>)> {
        self.inner.peek().map(|s| s.key)
                         .map(move |p| (p, ParamIter { param: p, inner: &mut self.inner }))
    }
}

pub struct ParamIter<'a, I: Iterator + 'a> {
    param: i64,
    inner: &'a mut Peekable<I>,
}

impl<'a, I> Iterator for ParamIter<'a, I>
    where I: Iterator<Item=StepItem> + 'a
{
    type Item = StepItem;

    fn next(&mut self) -> Option<Self::Item> {
        if let Some(true) = self.inner.peek().map(|s| s.key).map(|p| p == self.param) {
            self.inner.next()
        } else {
            None
        }
    }
}

fn main() {
    let con = PgConnection::establish(DB_URL)
        .expect(&format!("Error connecting to {}", DB_URL));
    let results = {
        use diesel::expression::sql;
        use diesel::types::BigInt;
        use schema::devices::{ table as devices, max_load_cc, max_poh, fail_date };
        let e = devices.select((max_load_cc, max_poh, sql::<BigInt>("sum(1) as total")))
                       .filter(fail_date.is_not_null())
                       .filter(max_load_cc.is_not_null())
                       .group_by((max_load_cc, max_poh))
                       .order((max_load_cc, max_poh))
                       .limit(1000);
        //print_sql!(e);
        e.load::<DevMaxParams>(&con).expect("Error loading posts!")
    }.into_iter().map(|dmp| StepItem {
                    key: dmp.max_load_cc.unwrap(),
                    val: Point { k: dmp.max_poh.unwrap(), v: dmp.total },
                });
    let mut points: Vec<(i64, Vec<Point<i64, i64>>)> = Vec::new();
    let mut steps = StepIter::new(results);
    points.push((0, vec![Point { k: 0, v: 0 }]));
    while let Some((p, pi)) = steps.next_step() {
        if p == 0 {
            let first = merge2d::merge(&points[0].1, pi.map(|item| item.val));
            points[0].1 = first;
            continue;
        }
        let last_new = merge2d::merge(&points.last().unwrap().1, pi.map(|item| item.val));
        points.push((p, last_new));
    }
    let max_y = points.last().unwrap().1.last().unwrap().k;
    for (x, pi) in points.into_iter() {
        let mut max_z = 0;
        for yz in pi {
            println!("{}\t{}\t{}", x, yz.k, yz.v);
            max_z = std::cmp::max(max_z, yz.v);
        }
        println!("{}\t{}\t{}", x, max_y, max_z);
    }
}
