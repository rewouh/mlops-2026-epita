from sklearn.linear_model import LinearRegression
import joblib
import pathlib

MODEL_PATH = pathlib.Path(__file__).parent / 'regression.joblib'

def format_l(v, width=64):
    v = int(round(v))
    return f'- {width}\'d{abs(v)}' if v < 0 else f'+ {width}\'d{v}'

def generate_v(model, module_name="g_linear_reg"):
    coefs = model.coef_
    intercept = model.intercept_

    n = len(coefs)

    lines = []
    lines.append(f"module {module_name}(")
    lines.append("    input [31:0] " + ", ".join([f"x{i}" for i in range(n)]) + ",")
    lines.append("    output [63:0] y")
    lines.append(");")
    lines.append("")

    for i in range(n):
        lines.append(f"    wire [63:0] p{i};")

    for i, coef in enumerate(coefs):
        coef_int = int(round(coef))
        lines.append(f"    multiplier32 mult{i} (.a(x{i}), .b(32'd{coef_int}), .p(p{i}));")

    sum_expr = " + ".join([f"p{i}" for i in range(n)])
    lines.append(f"    assign y = {sum_expr} {format_l(intercept)};")

    lines.append("endmodule")

    return "\n".join(lines)


if __name__ == "__main__":
    model = joblib.load(MODEL_PATH)
    # model = LinearRegression()

    # model.coef_ = [5000, 2000]
    # model.intercept_ = 10000

    vcode = generate_v(model)
    print(vcode)
