import flask
import lmfdb.utils
from flask import render_template, request

ZetaZeros = flask.Blueprint("zeta zeros", __name__, template_folder="templates")
logger = lmfdb.utils.make_logger(ZetaZeros)

from platt_zeros import *


@ZetaZeros.route("/")
def zetazeros():
    N = request.args.get("N", None, int)
    t = request.args.get("t", 0, float)
    limit = request.args.get("limit", 100, int)
    if limit > 1000:
        return list_zeros(N=N, t=t, limit=limit)
    else:
        return render_template('zeta.html', N=N, t=t, limit=limit, title="Zeros of $\zeta(s)$", bread=[('Zeros of $\zeta(s)$', ' '), ])


@ZetaZeros.route("/list")
def list_zeros(N=None,
               t=None,
               limit=None,
               fmt=None,
               download=None):
    if N is None:
        N = request.args.get("N", None, int)
    if t is None:
        t = request.args.get("t", 0, float)
    if limit is None:
        limit = request.args.get("limit", 100, int)
    if fmt is None:
        fmt = request.args.get("format", "plain")
    if download is None:
        download = request.args.get("download", "no")

    if limit < 0:
        limit = 100
    if N is not None:  # None is < 0!! WHAT THE WHAT!
        if N < 0:
            N = 0
    if t < 0:
        t = 0

    if limit > 100000:
        # limit = 100000
        return """hello downloader. you hurt the server :(
                  get the data here: http://www.lmfdb.org/data/zeros/zeta/ --
                  code how to read it is here: http://code.google.com/p/lmfdb/source/browse/#hg%2Fzeros%2Fzeta"""

    if N is not None:
        zeros = zeros_starting_at_N(N, limit)
    else:
        zeros = zeros_starting_at_t(t, limit)

    if fmt == 'plain':
        response = flask.Response(("%d %s\n" % (n, str(z)) for (n, z) in zeros))
        response.headers['content-type'] = 'text/plain'
        if download == "yes":
            response.headers['content-disposition'] = 'attachment; filename=zetazeros'
    else:
        response = str(list(zeros))

    return response
