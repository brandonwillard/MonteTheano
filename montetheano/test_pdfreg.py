import unittest
import numpy

import theano
from theano import tensor

from .pdfreg import pdf


def SRNG(seed=2345):
    return tensor.shared_randomstreams.RandomStreams(seed)


def test_normal_simple():
    s_rng = SRNG()
    n = s_rng.normal()

    p0 = pdf(n, 0)
    p1 = pdf(n, 1)
    pn1 = pdf(n, -1)

    f = theano.function([], [p0, p1, pn1])

    pvals = f()
    targets = numpy.asarray([
                1.0 / numpy.sqrt(2*numpy.pi),
                numpy.exp(-0.5) / numpy.sqrt(2*numpy.pi),
                numpy.exp(-0.5) / numpy.sqrt(2*numpy.pi),
                ])

    assert numpy.allclose(pvals,targets), (pvals, targets)


def test_normal_w_params():
    s_rng = SRNG()
    n = s_rng.normal(avg=2, std=3)

    p0 = pdf(n, 0)
    p1 = pdf(n, 2)
    pn1 = pdf(n, -1)

    f = theano.function([], [p0, p1, pn1])

    pvals = f()
    targets = numpy.asarray([
                numpy.exp(-0.5 * ((2.0/3.0)**2)) / numpy.sqrt(2*numpy.pi*9.0),
                numpy.exp(0) / numpy.sqrt(2*numpy.pi*9),
                numpy.exp(-0.5 * ((3.0/3.0)**2)) / numpy.sqrt(2*numpy.pi*9.0),
                ])

    assert numpy.allclose(pvals,targets), (pvals, targets)


def test_normal_nonscalar():
    raise NotImplementedError()


def test_normal_w_broadcasting():
    raise NotImplementedError()


def test_uniform_simple():
    s_rng = SRNG()
    u = s_rng.uniform()

    p0 = pdf(u, 0)
    p1 = pdf(u, 1)
    p05 = pdf(u, 0.5)
    pn1 = pdf(u, -1)

    f = theano.function([], [p0, p1, p05, pn1])

    pvals = f()
    targets = numpy.asarray([1.0, 1.0, 1.0, 0.0])

    assert numpy.allclose(pvals,targets), (pvals, targets)


def test_uniform_w_params():
    s_rng = SRNG()
    u = s_rng.uniform(low=-0.999, high=9.001)

    p0 = pdf(u, 0)
    p1 = pdf(u, 2)
    p05 = pdf(u, -1.5)
    pn1 = pdf(u, 10)

    f = theano.function([], [p0, p1, p05, pn1])

    pvals = f()
    targets = numpy.asarray([.1, .1, 0, 0])
    assert numpy.allclose(pvals,targets), (pvals, targets)


def test_uniform_nonscalar():
    raise NotImplementedError()


def test_uniform_w_broadcasting():
    raise NotImplementedError()
