import operator
import json
from ast import literal_eval
from aiohttp import web


class Calculator:
    def __init__(self):
        self.variables = {}

    def value(self, source):
        if not isinstance(source, str):
            return source

        try:
            return literal_eval(source)
        except ValueError:
            return self.variables[source]

    async def show_help(self, request):
        return web.Response(
            text="GET, PUT, or DELETE /var/[name], POST /add /subtract /multiply /divide"
        )

    async def op_load(self, request):
        try:
            return web.json_response(dict(value=self.value(request.match_info["name"])))
        except KeyError:
            return web.Response(status=404, text="Unknown variable")

    async def op_store(self, request):
        try:
            data = await request.json()
        except json.decoder.JSONDecodeError:
            return web.Response(status=400, text="Expected JSON")

        try:
            value = self.value(data["value"])
        except KeyError:
            return web.Response(status=422, text="Bad value for assignment")

        self.variables[request.match_info["name"]] = value

        return web.json_response(dict(value=value))

    async def op_delete(self, request):
        name = request.match_info["name"]

        if name in self.variables:
            del self.variables[name]
        else:
            return web.Response(status=404, text="Unknown variable")

    async def operation(self, request, operator):
        try:
            data = await request.json()
        except json.decoder.JSONDecodeError:
            return web.Response(status=400, text="Expected JSON")

        try:
            first = self.value(data['first'])
            second = self.value(data['second'])
        except KeyError:
            return web.Response(status=422, text="Bad operand")

        return web.json_response(dict(value = operator(first, second)))

    async def op_add(self, request):
        return await self.operation(request, operator.add)

    async def op_subtract(self, request):
        return await self.operation(request, operator.sub)

    async def op_multiply(self, request):
        return await self.operation(request, operator.mul)

    async def op_divide(self, request):
        return await self.operation(request, operator.truediv)
