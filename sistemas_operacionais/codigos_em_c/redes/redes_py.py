"""
Uso: python file.py <dominio-ou-host> 
"""
import sys
import socket
import ssl
import subprocess
import shutil
import tempfile
import os
from datetime import datetime
import idna

try:
    import dns.resolver
except Exception:
    print("Erro: instale dnspython: pip install dnspython")
    sys.exit(1)

try:
    import whois
except Exception:
    whois = None  

def print_section(title):
    print("\n" + "="*8 + " " + title + " " + "="*8)

def dns_lookup(host):
    resolver = dns.resolver.Resolver()
    types = ["A","AAAA","MX","NS","TXT"]
    results = {}
    for t in types:
        try:
            answers = resolver.resolve(host, t, lifetime=5)
            records = []
            for r in answers:
                records.append(r.to_text())
            results[t] = records
        except Exception as e:
            results[t] = []
    return results

def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None

def whois_info(domain):
    if whois is None:
        return "python-whois não instalado (pip install python-whois)"
    try:
        w = whois.whois(domain)
        return w
    except Exception as e:
        return f"Erro whois: {e}"

def get_leaf_cert_via_ssl(host, port):
    """Retorna PEM do certificado leaf usando ssl.get_server_certificate (string PEM)"""
    try:
        pem = ssl.get_server_certificate((host, port), timeout=5)
        return pem
    except Exception as e:
        return None

def parse_pem_with_openssl(pem_blob):
    """Se openssl existir, passa o PEM para 'openssl x509' para extrair subject, issuer, dates, SANs"""
    if shutil.which("openssl") is None:
        return None
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as tf:
        tf.write(pem_blob)
        tf.flush()
        fname = tf.name
    try:
        cmd = ["openssl", "x509", "-noout", "-subject", "-issuer", "-dates", "-text", "-certopt", "no_pubkey,no_sigdump"]
        proc = subprocess.run(cmd, input=open(fname,"rb").read(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = proc.stdout.decode(errors="ignore")
        return out
    except Exception as e:
        return f"Erro ao chamar openssl: {e}"
    finally:
        try:
            os.unlink(fname)
        except Exception:
            pass

def get_chain_via_openssl(host, port):
    """Tenta recuperar a cadeia via 'openssl s_client -showcerts' e separar os certificados"""
    if shutil.which("openssl") is None:
        return None
    cmd = ["openssl", "s_client", "-showcerts", "-connect", f"{host}:{port}", "-servername", host]
    try:
        proc = subprocess.run(cmd, input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        data = proc.stdout.decode(errors="ignore") + proc.stderr.decode(errors="ignore")
    except Exception as e:
        return None

    # Extrai blocos PEM -----BEGIN CERTIFICATE----- ... -----END CERTIFICATE-----
    pem_blocks = []
    start = "-----BEGIN CERTIFICATE-----"
    end = "-----END CERTIFICATE-----"
    idx = 0
    while True:
        s = data.find(start, idx)
        if s == -1:
            break
        e = data.find(end, s)
        if e == -1:
            break
        pem = data[s:e+len(end)]
        pem_blocks.append(pem)
        idx = e + len(end)
    return pem_blocks

def traceroute(host):
    """Chama traceroute/tracepath/tracert conforme SO disponível"""
    if shutil.which("traceroute"):
        cmd = ["traceroute", "-n", host]
    elif shutil.which("tracepath"):
        cmd = ["tracepath", host]
    elif shutil.which("tracert"):
        cmd = ["tracert", "-d", host]
    else:
        return "Nenhum utilitário de traceroute encontrado (traceroute/tracepath/tracert)"
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
        return proc.stdout.decode(errors="ignore")
    except Exception as e:
        return f"Erro ao executar traceroute: {e}"

def main():
    if len(sys.argv) < 2:
        print("Uso: python recon_infra.py <dominio-ou-host> [porta]")
        sys.exit(1)
    target_raw = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 443

    # IDNA encode if necessário
    try:
        target = idna.encode(target_raw).decode()
    except Exception:
        target = target_raw

    print_section(f"Resumo: {target}:{port}")
    print(f"Alvo (IDNA): {target}")

    # DNS lookups
    print_section("DNS")
    dns_res = dns_lookup(target)
    for t, recs in dns_res.items():
        print(f"{t}:")
        if recs:
            for r in recs:
                print("  -", r)
        else:
            print("  - (nenhum)")

    # Resolve IPs (A/AAAA)
    print_section("Resolução de IPs e reverse DNS")
    ips = set()
    for r in dns_res.get("A", []):
        # r pode ter TTL etc mas em geral é só IP
        ips.add(r.split()[0])
    for r in dns_res.get("AAAA", []):
        ips.add(r.split()[0])
    if not ips:
        # fallback: getaddrinfo
        try:
            for res in socket.getaddrinfo(target, None):
                ips.add(res[4][0])
        except Exception:
            pass
    if not ips:
        print("Nenhum IP encontrado")
    else:
        for ip in ips:
            rev = reverse_dns(ip)
            print(f"{ip}  reverse: {rev}")

    # WHOIS
    print_section("WHOIS")
    domain_for_whois = target_raw
    # tenta extrair só o domínio (simples): remove subdomínio
    try:
        parts = target_raw.split(".")
        if len(parts) >= 2:
            domain_for_whois = ".".join(parts[-2:])
    except Exception:
        domain_for_whois = target_raw
    wi = whois_info(domain_for_whois)
    print(wi)

    # TLS / Cert
    print_section("TLS / Certificado (leaf)")
    pem = get_leaf_cert_via_ssl(target, port)
    if pem:
        print("Leaf certificate (PEM) obtido via ssl.get_server_certificate().")
        # tenta extrair informações com openssl se disponível
        parsed = parse_pem_with_openssl(pem)
        if parsed:
            print(parsed)
        else:
            # fallback: apenas mostra PEM (cuidado: grande)
            print("openssl CLI não disponível: exibindo PEM do certificado leaf (resumido).")
            print("\n".join(pem.splitlines()[:10]) + "\n... (truncated) ...")
    else:
        print("Não foi possível obter o certificado leaf via ssl.get_server_certificate()")

    # Cadeia via openssl (opcional)
    print_section("Cadeia TLS via openssl (se disponível)")
    chain = get_chain_via_openssl(target, port)
    if chain is None:
        print("openssl s_client não disponível ou falhou. Não foi possível recuperar cadeia completa.")
    elif not chain:
        print("Nenhum bloco PEM encontrado na saída do s_client.")
    else:
        print(f"Certificados na cadeia: {len(chain)}\n")
        for i, pem_block in enumerate(chain, 1):
            print(f"--- Cert #{i} ---")
            parsed = parse_pem_with_openssl(pem_block)
            if parsed:
                print(parsed)
            else:
                print("(não foi possível parsear com openssl)")

    # Traceroute
    print_section("Traceroute")
    tr = traceroute(target)
    print(tr)

    print_section("Fim")

if __name__ == "__main__":
    main()
