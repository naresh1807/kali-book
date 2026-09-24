"""Transaction-correlation model only: not OAuth/OIDC or a JWT verifier."""
import hmac

def bound_response(expected, response):
    required=('state','nonce','issuer','audience')
    if any(not isinstance(response.get(k),str) or not isinstance(expected.get(k),str) for k in required):return False
    return all(hmac.compare_digest(expected[k].encode(),response[k].encode()) for k in required)

if __name__=='__main__':
    expected={'state':'lab-transaction','nonce':'lab-nonce','issuer':'https://issuer.example','audience':'lab-client'}
    print('matched transaction:',bound_response(expected,dict(expected)))
    for key in expected:
        print('changed '+key+':',bound_response(expected,{**expected,key:'wrong'}))
