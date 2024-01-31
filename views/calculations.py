from flask import render_template,request, Blueprint
from xray_models import Compound, Density
from forms import OptConstForm
from views.x_ray_mirrors.plotters import OptConstPlotter


calc = Blueprint('calc', __name__, url_prefix='/calc')


@calc.route('/beta-delta', methods=["POST", "GET"])
def beta_delta():
    plotter = OptConstPlotter()

    # download all available elements and compounds from the databases
    choices_comp = [(c.formula, f'{c.formula} ({c.density:.1f} г/см3)') for c in Compound.query
                    .join(Density, onclause=Compound.id == Density.compound_id)
                    .add_columns(Compound.formula, Density.density)
                    .filter((Density.density.isnot(None)) & (~Compound.formula.contains('∙'))
                                                          & (~Compound.formula.contains('(')))
                    .all()]

    opt_const_form = OptConstForm()
    opt_const_form.materials.choices = choices_comp

    if request.method == "POST":
        energy = float(request.form.get('energy'))
        compounds = request.form.getlist('materials')
        graph = plotter.plot_opt_consts(compounds, energy)
    else:
        graph = plotter.plot_opt_consts([], 100)

    return render_template("beta_delta.html", title="Оптические константы", opt_const_form=opt_const_form,
                           plot=graph)
