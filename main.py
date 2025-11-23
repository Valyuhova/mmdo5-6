import math

def f(x, y):
    return 1 + 15*x - 2*(x**2) - x*y - 2*(y**2)


def exploratory_search(base_point, h):
    x, y = base_point
    best_val = f(x, y)

    val_plus = f(x + h, y)
    val_minus = f(x - h, y)
    if val_plus > best_val:
        x = x + h
        best_val = val_plus
    elif val_minus > best_val:
        x = x - h
        best_val = val_minus

    val_plus = f(x, y + h)
    val_minus = f(x, y - h)
    if val_plus > best_val:
        y = y + h
        best_val = val_plus
    elif val_minus > best_val:
        y = y - h
        best_val = val_minus

    return (x, y), best_val


def hooke_jeeves_max(x0=0.0, y0=0.0, h=1.0, eps=0.1):
    b = (x0, y0)
    fb = f(*b)
    history = []

    k = 1
    while h >= eps:
        new_point, f_new = exploratory_search(b, h)

        history.append({
            "iter": k,
            "h": h,
            "base": b,
            "f_base": fb,
            "explore": new_point,
            "f_explore": f_new,
            "pattern": None,
            "f_pattern": None,
            "accepted": None
        })

        if f_new > fb:
            p = (new_point[0] + (new_point[0] - b[0]),
                 new_point[1] + (new_point[1] - b[1]))
            fp = f(*p)

            history[-1]["pattern"] = p
            history[-1]["f_pattern"] = fp

            if fp > f_new:
                b, fb = p, fp
                history[-1]["accepted"] = "pattern"
            else:
                b, fb = new_point, f_new
                history[-1]["accepted"] = "explore"
        else:
            h /= 2
            history[-1]["accepted"] = "shrink_h"

        k += 1

    return b, fb, history


def print_history(history):
    for step in history:
        print(f"Ітерація {step['iter']}   (h = {step['h']})")
        print(f" b = {step['base']},  f(b) = {step['f_base']:.6g}")
        print(f" b' = {step['explore']},  f(b') = {step['f_explore']:.6g}")

        if step["pattern"] is not None:
            print(f" P = {step['pattern']},  f(P) = {step['f_pattern']:.6g}")

        print(f" {step['accepted']}")
        print("-"*60)


if __name__ == "__main__":
    x0, y0 = 0, 0
    h0 = 1
    eps = 0.1

    point_max, f_max, hist = hooke_jeeves_max(x0, y0, h0, eps)

    print_history(hist)
    
    print("\nВІДПОВІДЬ:")
    print(f"Точка максимуму: {point_max}")
    print(f"fmax = {f_max}")