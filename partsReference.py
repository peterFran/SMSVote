– C: mobile station (client)
– S: Authentication Source (server)
– U: cell phone number +44 20 3322 9681
– H: HMAC_SHA256 (U || PIN || Q), where Q is given by the C
– D: symmetric  key generating parameters
– Dn: D generated on a new nth session
– Q: new session identifier
– Qn: Q generated on a new nth session
– Rc: fresh random challenge from C (64-bits) rand (64bits)
– Pf: an unused private port number f
– M: message
– SQ: sequence number
– HU: HMAC_SHA256 (U) SMSSec.hashText(+442033229681)
– HUn: HU generated on a new nth session
– PK: public  key of the server (2048-bits)
– SK: symmetric  key (256-bits)
– SK_n: an SK generated from using Dn
– {}PK: RSA_OAEP encryption using PK
– {}SK: symmetric  key encryption using AES/Counter Mode – {}SK_n: symmetric  key encryption using the SK_n key
- PIN: personal identification number that is known to both the C and the S - machine num

computers & security 27 (2008) 154–167 159
￼M1: CPz /SPz :
{U||H||SK||Rc}PK
