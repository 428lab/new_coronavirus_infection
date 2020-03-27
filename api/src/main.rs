#![feature(proc_macro_hygiene)]
#![feature(decl_macro)]

#[macro_use]
extern crate rocket;

mod models;
mod routes;

// WebAPIのURLルーティングはroutes.rsに移動する
use routes::*;

// rocketにルーティングをマウントして、開始する。
fn main() {
    rocket::ignite()
        .mount("/", routes![index, todos, new_todo, todo_by_id,todos_accepted])
        .launch();
}