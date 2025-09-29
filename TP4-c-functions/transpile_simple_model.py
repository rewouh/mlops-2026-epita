import joblib
import pathlib
import numpy as np
import sys
import os
import subprocess
from sklearn.linear_model import LogisticRegression

MODEL_PATH = pathlib.Path(__file__).parent / 'regression.joblib'

def generate_c_code(coefs, intercept):
    thetas = [intercept] + list(coefs)
    thetas_str = ", ".join(f"{t:.6f}f" for t in thetas)
    
    code = f"""
#include <stdio.h>
#include <math.h>

float sigmoid(float x) {{
    return 1.0f / (1.0f + expf(-x));
}}

float linear_regression_prediction(float* features, float* thetas, int n_parameters) {{
    float result = thetas[0];
    for (int i = 1; i < n_parameters; i++) {{
        result += thetas[i] * features[i - 1];
    }}
    return result;
}}

float logistic_regression(float* features, float* thetas, int n_parameter) {{
    float z = linear_regression_prediction(features, thetas, n_parameter);

    printf("z = %f\\n", z);
    printf("sigmoid input = %f\\n", -z);
    printf("expf(-z) = %f\\n", expf(-z));

    return sigmoid(z);
}}

int simple_tree(float *features, int n_features) {{
    if (features[0] > 0) {{
        return 0;
    }} else if (features[1] > 0) {{
        return 0;
    }} else {{
        return 1;
    }}
}}

int main() {{
    float features[7] = {{ 205.999169f, 2.0f, 0.0f, 0.0f, 0.0f, 0.0f, 1.0f }};
    float thetas[8] = {{ {thetas_str} }};
    
    float y = linear_regression_prediction(features, thetas, 8);
    printf("Prediction = %f\\n", y);
    return 0;
}}
"""
    return code

def main():
    model = joblib.load(MODEL_PATH)
    
    coefs = model.coef_.ravel()
    intercept = model.intercept_.ravel()[0]

    code = generate_c_code(coefs, intercept)
    
    c_file = "generated.c"
    with open(c_file, "w") as f:
        f.write(code)
    
    print(f"Generated {c_file}")
    compile_cmd = f"gcc -o generated {c_file} -lm"
    print("Compile cmd:", compile_cmd)
    
    subprocess.run(compile_cmd, shell=True)

if __name__ == "__main__":
    main()
