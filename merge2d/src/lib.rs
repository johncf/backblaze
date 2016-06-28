#[derive(Debug, PartialEq)]
pub struct Point<X, Y> {
    x: X,
    y: Y,
}

fn newx_lasty_mut(res: &mut Vec<Point<u32, i32>>, x: u32) -> &mut i32 {
    let (last_x, last_y) = res.last().map(|p| (Some(p.x), p.y)).unwrap_or((None, 0));
    match last_x {
        Some(last_x) if last_x == x => (),
        _ => res.push(Point {
            x: x,
            y: last_y,
        }),
    }
    res.last_mut().map(|p| &mut p.y).unwrap()
}

pub fn merge(base: &Vec<Point<u32, i32>>, add: &Vec<Point<u32, i32>>) -> Vec<Point<u32, i32>> {
    let mut res = Vec::new();
    let mut ai = add.iter().peekable();
    let mut add_ysum = 0;
    for b in base {
        while let Some(true) = ai.peek().map(|&a| b.x >= a.x) {
            let a = ai.next().unwrap();
            *newx_lasty_mut(&mut res, a.x) += a.y;
            add_ysum += a.y;
        }
        *newx_lasty_mut(&mut res, b.x) = b.y + add_ysum;
    }
    while let Some(a) = ai.next() {
        *newx_lasty_mut(&mut res, a.x) += a.y;
    }
    res
}

#[cfg(test)]
mod tests {
    use super::{merge, Point};

    #[test]
    fn it_works() {
        let b = vec![
            Point { x: 5, y: 2 },
            Point { x: 6, y: 3 },
            Point { x: 7, y: 4 },
        ];
        let a = vec![
            Point { x: 2, y: 1 },
            Point { x: 5, y: 2 },
            Point { x: 9, y: -3 },
        ];
        assert_eq!(merge(&b, &a), vec![
            Point { x: 2, y: 1 },
            Point { x: 5, y: 5 },
            Point { x: 6, y: 6 },
            Point { x: 7, y: 7 },
            Point { x: 9, y: 4 },
        ])
    }
}
