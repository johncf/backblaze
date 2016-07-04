#![feature(custom_derive, custom_attribute, plugin)]
#![plugin(diesel_codegen)]

#[macro_use]
extern crate diesel;
extern crate merge2d;

pub const DB_URL: &'static str = "postgres://localhost/backblaze2";

pub mod schema;

use diesel::prelude::*; // alot of traits + diesel::result::*
use diesel::pg::PgConnection;

#[derive(Debug, Queryable)]
pub struct DevMaxParams {
    max_load_cc: Option<i64>,
    max_poh: Option<i64>,
    total: i64,
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
                       .limit(5);
        //print_sql!(e);
        e.load::<DevMaxParams>(&con).expect("Error loading posts!")
    };
    for d in results {
        println!("{:?}", d);
    }
}
