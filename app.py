from shiny import App, render, ui, reactive
import requests
import logging

api_url = "http://127.0.0.1:8080/predict"
headers = {"Content-Type": "application/json"}


logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)

api_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar(
            [ui.input_slider("bill_length",
                             "Bill Length (mm)",
                             min=30,
                             max=60,
                             value=45,
                             step=0.1),
             ui.input_select("sex", "Sex",
                             choices=["Male", "Female"]),
             ui.input_select("species", "Species",
                             choices=["Adelie", "Chinstrap", "Gentoo"]),
             ui.input_action_button("predict", "Predict")]
        ),

        ui.h3("Penguin Parameters"),

        ui.output_text("bill_length_out"),
        ui.output_text("sex_out"),
        ui.output_text("species_out"),

        ui.h3("Predicted Penguin Mass (g)"),
        ui.output_text("pred_out"),
    ),
    title="Penguin Mass Predictor",
)


def server(input, output, session):
    logging.info("App start")

    @render.text
    def bill_length_out():
        return f"Bill Length (mm): {input.bill_length()}"

    @render.text
    def sex_out():
        return f"Sex: {input.sex()}"

    @render.text
    def species_out():
        return f"Species: {input.species()}"

    @reactive.Calc
    def vals():
        d = [{
            "bill_length_mm": input.bill_length(),
            "sex_male": input.sex() == "Male",
            "species_Gentoo": input.species() == "Gentoo",
            "species_Chinstrap": input.species() == "Chinstrap"
        }]

        return d

    @reactive.Calc
    @reactive.event(input.predict)
    def pred():
        logging.info("Request Made")
        r = requests.post(api_url, json=vals())
        if r.status_code != 200:
            logging.error(f"Bad Request. HTTP error returned.\
                          Status Code: {r.status_code}")
            print(f"Status Code: {r.status_code}")
            print(f"Request: {r.headers}")
            print(f"Request: {r.content}")
            return "Bad Request"

        logging.info("Request Returned")
        return r.json().get('predict')[0]

    @output
    @render.text
    def vals_out():
        return f"{vals()}"

    @output
    @render.text
    def pred_out():
        return f"{round(pred(), 3)}"


app = App(api_ui, server)
