import theano
import rv
from rv import Normal
from fg import posterior_modes

def test_gaussian_ml():
    """Maximum likelihood fitting of Gaussian"""

    x = Normal(0, 1)
    data = theano.shared.as_tensor_variable([0, 1, 3, 4])

    post = posterior_modes({x: data})
    ml_mu = post[x.mu]
    ml_sigma = post[x.sigma]

    f = theano.function([], ml_mu, ml_sigma)

def test_gaussian_map():
    """Maximum a-posteriori fitting of Gaussian"""

    x = Normal(
            mu=Normal(10, .1),
            sigma=1)
    data = theano.shared.as_tensor_variable([0, 1, 3, 4])

    post = posterior_modes({x: data})
    map_mu = post[x.mu]
    map_sigma = post[x.sigma]

    f = theano.function([], [map_mu, map_sigma])

def test_gaussian_tied():
    """Maximum a-posteriori fitting of Gaussian in DAG"""

    y = Normal(0, 1)
    x = Normal(mu=y, sigma=2**y)

    data = theano.shared.as_tensor_variable([0, 1, 3, 4])

    post = posterior_modes({x: data})
    map_y = post[y]

    f = theano.function([], map_y)



def test_rbm():

    n_vis = 6
    n_hid = 5

    w = tensor.matrix(shape=(n_vis, n_hid))

    v = bernoulli(n_vis)
    h = bernoulli(n_hid)
    E = tensor.dot(v, w, h)

    # E is now a random variable in a directed graphical model
    # TODO: how do we get from here to a gibbs sampler in easy logical steps?