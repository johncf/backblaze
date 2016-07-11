extern crate merge2d;

pub const DB_URL: &'static str = "postgres://john@localhost/backblaze2";

extern crate postgres;

use postgres::{Connection, SslMode};
use merge2d::Point;
use std::iter::Peekable;

#[derive(Debug)]
pub struct DevMaxParams {
    max_load_cc: i64,
    max_poh: i64,
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
    let con = Connection::connect(DB_URL, SslMode::None)
        .expect(&format!("Error connecting to {}", DB_URL));
    let rows = &con.query("SELECT max_load_cc, max_poh, sum(1) as total FROM devices WHERE \
                          fail_date IS NOT NULL AND max_load_cc IS NOT NULL \
                          GROUP BY max_load_cc, max_poh ORDER BY max_load_cc, max_poh LIMIT 1000", &[])
                   .expect("Error loading posts!");
    let results = rows.iter().map(|row| StepItem {
        key: row.get("max_load_cc"),
        val: Point { k: row.get("max_poh"), v: row.get("total") },
    });
    let mut points: Vec<(i64, Vec<Point<i64, i64>>)> = Vec::new();
    let mut steps = StepIter::new(results);
    points.push((0, vec![Point { k: 0, v: 0 }]));
    while let Some((p, pi)) = steps.next_step() {
        let last_new = merge2d::merge(&points.last().unwrap().1, pi.map(|item| item.val));
        if p == 0 {
            points[0].1 = last_new;
        } else {
            points.push((p, last_new));
        }
    }
    let max_y = points.last().unwrap().1.last().unwrap().k;
    for (x, pi) in points {
        let mut max_z = 0;
        for yz in pi {
            println!("{}\t{}\t{}", x, yz.k, yz.v);
            max_z = std::cmp::max(max_z, yz.v);
        }
        println!("{}\t{}\t{}", x, max_y, max_z);
    }
}
