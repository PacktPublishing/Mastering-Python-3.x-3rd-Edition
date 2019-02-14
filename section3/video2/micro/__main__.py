from aiohttp import web
from .calculator import Calculator

def main():
    calc = Calculator()

    app = web.Application()

    app.add_routes([
        web.get('/', calc.show_help),

        web.get('/var/{name}', calc.op_load),
        web.put('/var/{name}', calc.op_store),
        web.delete('/var/{name}', calc.op_delete),

        web.post('/add', calc.op_add),
        web.post('/subtract', calc.op_subtract),
        web.post('/multiply', calc.op_multiply),
        web.post('/divide', calc.op_divide),
    ])

    web.run_app(app)

if __name__ == '__main__':
    main()
