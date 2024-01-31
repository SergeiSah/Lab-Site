from flask import render_template, redirect, url_for, request, jsonify, Blueprint
from xray_models import Compound
from forms import OptConstForm
from plotters import OptConstPlotter


calc = Blueprint('calc', __name__, url_prefix='/calc')


@calc.route('/beta-delta', methods=["POST", "GET"])
def beta_delta():
    plotter = OptConstPlotter()

    # download all available elements and compounds from the databases
    choices_comp = [(c.formula, c.formula) for c in Compound.query.all()]

    opt_const_form = OptConstForm()
    opt_const_form.materials.choices = choices_comp

    if request.method == "POST":
        energy = float(request.form.get('energy'))
        compounds = request.form.getlist('materials')
        graph = plotter.plot_opt_consts(compounds, energy)
    else:
        graph = plotter.plot_opt_consts([], 112)

    return render_template("beta_delta.html", title="Оптические константы", opt_const_form=opt_const_form,
                           plot=graph)
