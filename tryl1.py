import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from PIL import Image

def beer_law(x, A, b):
    return A * x + b

def calculate_concentration(absorbance, slope, intercept):
    return (absorbance - intercept) / slope

def main():
    st.title("EXPERIMENT - 4")

    # Image paths
    image_paths = ["exp4_1.png", "exp4_2.png", "exp4_3.png"]

    # Display images using Streamlit
    for img_path in image_paths:
        img = Image.open(img_path)
        st.image(img, use_column_width=True)

    # Part B: Determination of λmax
    st.header("Part B: Determination of λmax")

    # Input for Wavelength and Absorbance
    st.subheader("Enter Wavelength and Absorbance for different filters (one pair per line, comma-separated):")
    default_input_b = "400, 0.2\n420, 0.5\n470, 0.8\n500, 1.0\n530, 0.9\n620, 0.6\n660, 0.4\n700, 0.2"
    input_text_lambda_max = st.text_area("Example:\n" + default_input_b, value=default_input_b)

    if input_text_lambda_max:
        input_lines = input_text_lambda_max.split('\n')
        data_lambda_max = {'Wavelength': [], 'Absorbance': []}

        for line in input_lines:
            parts = line.split(',')
            if len(parts) == 2:
                wavelength, absorbance = map(float, parts)
                data_lambda_max['Wavelength'].append(wavelength)
                data_lambda_max['Absorbance'].append(absorbance)

        data_lambda_max = pd.DataFrame(data_lambda_max)

        # Display the data
        st.subheader("Data for λmax Determination:")
        st.write(data_lambda_max)

        # Select λmax
        lambda_max = st.selectbox("Select λmax (wavelength corresponding to highest Absorbance):", data_lambda_max['Wavelength'])

    # Part C: Determination of A and %T for known and unknown concentration
    st.header("Part C: Determination of A and %T for known and unknown concentration")

    # Input for concentration and absorbance
    st.subheader("Enter Concentration and Absorbance (one pair per line, comma-separated):")
    default_input_c = "0.002, 0.4\n0.004, 0.6\n0.006, 0.8\n0.008, 1.0\n0.010, 1.2"
    input_text_concentration = st.text_area("Example:\n" + default_input_c, value=default_input_c)

    if input_text_concentration:
        input_lines = input_text_concentration.split('\n')
        data_concentration = {'Concentration': [], 'Absorbance': []}

        for line in input_lines:
            parts = line.split(',')
            if len(parts) == 2:
                concentration, absorbance = map(float, parts)
                data_concentration['Concentration'].append(concentration)
                data_concentration['Absorbance'].append(absorbance)

        data_concentration = pd.DataFrame(data_concentration)

        # Display the data
        st.subheader("Data for A and %T Determination:")
        st.write(data_concentration)

        # Fit Beer's Law only if data is available
        if 'Concentration' in data_concentration.columns and 'Absorbance' in data_concentration.columns:
            # Fit Beer's Law
            popt, pcov = curve_fit(beer_law, data_concentration['Concentration'], data_concentration['Absorbance'])

            # Display the fitted parameters
            st.subheader("Beer's Law Parameters:")
            st.write(f"A (slope): {popt[0]}")
            st.write(f"b (intercept): {popt[1]}")

            # Results for known concentrations
            st.subheader("Results for Known Concentrations:")
            st.write("Sr No | Conc. of solution(C) | Absorbance (A) | Transmission (%T)")
            for i, row in data_concentration.iterrows():
                concentration = row['Concentration']
                absorbance = row['Absorbance']
                transmission = 100 - absorbance
                st.write(f"{i + 1} | {concentration} | {absorbance} | {transmission}")

            # Results for unknown concentration
            st.subheader("Results for Unknown Concentration:")
            unknown_absorbance = st.number_input("Enter absorbance for unknown concentration:")
            unknown_transmission = 100 - unknown_absorbance
            st.write(f"Unknown | {calculate_concentration(unknown_absorbance, *popt)} | {unknown_absorbance} | {unknown_transmission}")

    # Absorbance vs. Wavelength graph
    st.subheader("Absorbance vs. Wavelength Graph:")
    if 'Wavelength' in data_lambda_max.columns and 'Absorbance' in data_lambda_max.columns:
        plt.figure(figsize=(8, 6))
        plt.plot(data_lambda_max['Wavelength'], data_lambda_max['Absorbance'], marker='o', linestyle='-', color='b')
        plt.title("Absorbance vs. Wavelength")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Absorbance (O.D)")
        st.pyplot(plt)
    else:
        st.warning("Insufficient data for plotting. Please provide data for λmax determination.")

    # Absorbance vs. Concentration graph
    st.subheader("Absorbance vs. Concentration Graph:")
    if 'Concentration' in data_concentration.columns and 'Absorbance' in data_concentration.columns:
        plt.figure(figsize=(8, 6))
        plt.plot(data_concentration['Concentration'], data_concentration['Absorbance'], marker='o', linestyle='-', color='r')
        plt.title("Absorbance vs. Concentration")
        plt.xlabel("Concentration [in MOLAR]")
        plt.ylabel("Absorbance (O.D)")
        st.pyplot(plt)
    else:
        st.warning("Insufficient data for plotting. Please provide data for A and %T determination.")

if __name__ == "__main__":
    main()
