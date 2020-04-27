import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utilities_s8_gross_return import *

def entropy_moment_bounds_s8():
    # Solve the minimization problems over a grid of ξ
    tol = 2e-10
    max_iter = 1000

    solver_s8 = InterDivConstraint(tol,max_iter)

    # Grid for ξ
    ξ_grid = np.arange(.01,1.01,.01)
    results_lower = []
    results_upper = []

    μs = np.zeros_like(ξ_grid)
    REs = np.zeros_like(ξ_grid)
    bounds = np.zeros_like(ξ_grid)
    bounds_cond_1 = np.zeros_like(ξ_grid)
    bounds_cond_2 = np.zeros_like(ξ_grid)
    bounds_cond_3 = np.zeros_like(ξ_grid)
    ϵs = np.zeros_like(ξ_grid)
    
    results_lower = [None]*len(ξ_grid)
    results_upper = [None]*len(ξ_grid)
    
    for i in range(len(ξ_grid)):
        ξ = ξ_grid[i]
        temp = solver_s8.iterate(ξ,lower=True)
        results_lower[i] = temp
        temp = solver_s8.iterate(ξ,lower=False)
        results_upper[i] = temp

    REs = np.array([result['RE'] for result in results_lower])
    REs_cond = np.array([result['RE_cond'] for result in results_lower])
    moment_bounds_cond_lower = np.log(np.array([result['moment_bound_cond'] for result in results_lower]))
    moment_bounds_cond_upper = np.log(np.array([result['moment_bound_cond'] for result in results_upper]))
    moment_bounds_lower = np.log(np.array([result['moment_bound'] for result in results_lower]))
    moment_bounds_upper = np.log(np.array([result['moment_bound'] for result in results_upper]))
    moment_cond = np.log(np.array([result['moment_cond'] for result in results_lower]))
    moment = np.log(np.array([result['moment'] for result in results_lower]))

    # Plots for RE and E[Mg(X)]
    fig = make_subplots(rows=1, cols=2)
    fig.add_trace(
        go.Scatter(x=ξ_grid, y=REs, name='E[MlogM]', line=dict(color='blue')),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=ξ_grid, y=np.ones_like(ξ_grid)*REs[-1]*1.1, name='1.1x minimum RE', line=dict(color='black',dash='dash')),
        row=1, col=1
    )


    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_bounds_lower, name='log E[Mg(X)], lower bound', line=dict(color='green')),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_bounds_upper, name='log E[Mg(X)], upper bound', line=dict(color='red')),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment, name='log E[g(X)]',line=dict(dash='dash')),
        row=1, col=2
    )


    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_bounds_cond_lower[:,0], name='log E[Mg(X)|state 1], lower bound', visible=False, line=dict(color='green')),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_bounds_cond_upper[:,0], name='log E[Mg(X)|state 1], upper bound', visible=False, line=dict(color='red')),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_cond[:,0], name='log E[g(X)|state 1]', visible=False, line=dict(dash='dash')),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_bounds_cond_lower[:,1], name='log E[Mg(X)|state 2], lower bound', visible=False, line=dict(color='green')),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_bounds_cond_upper[:,1], name='log E[Mg(X)|state 2], upper bound', visible=False, line=dict(color='red')),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_cond[:,1], name='log E[g(X)|state 2]', visible=False, line=dict(dash='dash')),
        row=1, col=2
    )


    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_bounds_cond_lower[:,2], name='log E[Mg(X)|state 3], lower bound', visible=False, line=dict(color='green')),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_bounds_cond_upper[:,2], name='log E[Mg(X)|state 3], upper bound', visible=False, line=dict(color='red')),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=ξ_grid, y=moment_cond[:,2], name='log E[g(X)|state 3]', visible=False, line=dict(dash='dash')),
        row=1, col=2
    )


    fig.update_layout(height=400, width=1000, title_text="Relative entropy (left) and moment bounds (right)", showlegend = False)
    fig.update_xaxes(rangemode="tozero",title_text='ξ')
    fig.update_yaxes(rangemode="tozero")

    # fig['layout']['xaxis'+str(int(1))].update(range = (0,0.2))
    fig['layout']['yaxis'+str(int(1))].update(range = (0.,0.06))
    fig['layout']['xaxis'+str(int(2))].update(range = (0.,1.))
    fig['layout']['yaxis'+str(int(2))].update(range = (-0.01,0.04))

    # Add button
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="up",
                active=0,
                x=1.2,
                y=0.9,
                buttons=list([
                    dict(label="Unconditional",
                         method="update",
                         args=[{"visible": [True]*5 + [False]*15 }]),
                    dict(label="State 1",
                         method="update",
                         args=[{"visible": [True]*2 + [False]*3 + [True]*3 + [False]*6}]),
                    dict(label="State 2",
                         method="update",
                         args=[{"visible": [True]*2 + [False]*6 + [True]*3 + [False]*3}]),
                    dict(label="State 3",
                         method="update",
                         args=[{"visible": [True]*2 + [False]*9 + [True]*3}]),
                ]),
            )
        ])


    fig.show()
    
    