use std::ops::{Add, AddAssign};

#[derive(Debug, PartialEq)]
pub struct Point<K, V> {
    pub k: K,
    pub v: V,
}

fn newk_lastv_mut<K, V>(res: &mut Vec<Point<K, V>>, k: K) -> &mut V
    where K: Copy + Eq, V: Copy + Default
{
    let (last_k, last_v) = res.last().map(|p| (Some(p.k), p.v)).unwrap_or((None, V::default()));
    match last_k {
        Some(last_k) if last_k == k => (),
        _ => res.push(Point {
            k: k,
            v: last_v,
        }),
    }
    res.last_mut().map(|p| &mut p.v).unwrap()
}

pub fn merge<K, V, I>(base: &Vec<Point<K, V>>, add: I) -> Vec<Point<K, V>>
    where K: Copy + Ord,
          V: Add<Output=V> + AddAssign + Copy + Default,
          I: IntoIterator<Item=Point<K, V>>,
{
    let mut res = Vec::new();
    let mut ai = add.into_iter().peekable();
    let mut add_vsum = V::default();
    for b in base {
        while let Some(true) = ai.peek().map(|a| b.k >= a.k) {
            let a = ai.next().unwrap();
            *newk_lastv_mut(&mut res, a.k) += a.v;
            add_vsum += a.v;
        }
        *newk_lastv_mut(&mut res, b.k) = b.v + add_vsum;
    }
    while let Some(a) = ai.next() {
        *newk_lastv_mut(&mut res, a.k) += a.v;
    }
    res
}

#[cfg(test)]
mod tests {
    use super::{merge, Point};

    #[test]
    fn it_works() {
        let b = vec![
            Point { k: 5, v: 2 },
            Point { k: 6, v: 3 },
            Point { k: 7, v: 4 },
        ];
        let a = vec![
            Point { k: 2, v: 1 },
            Point { k: 5, v: 2 },
            Point { k: 9, v: -3 },
        ];
        assert_eq!(merge(&b, a), vec![
            Point { k: 2, v: 1 },
            Point { k: 5, v: 5 },
            Point { k: 6, v: 6 },
            Point { k: 7, v: 7 },
            Point { k: 9, v: 4 },
        ])
    }
}
