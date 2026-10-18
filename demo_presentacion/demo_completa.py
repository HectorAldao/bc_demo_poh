import hashlib

MUESTRA = 8


def hash_sha256(datos):
    return hashlib.sha256(datos).hexdigest()


def titulo(texto):
    print("\n" + "=" * 64)
    print(texto)
    print("=" * 64)


def generar_secuencia(semilla, n):
    secuencia = []
    anterior = semilla.encode()
    for i in range(1, n + 1):
        actual = hash_sha256(anterior)
        secuencia.append((i, actual, None))
        anterior = actual.encode()
    return secuencia


def insertar_eventos(semilla, n, eventos):
    secuencia = []
    anterior = semilla.encode()
    for i in range(1, n + 1):
        evento = eventos.get(i)
        datos = anterior if evento is None else anterior + evento.encode()
        actual = hash_sha256(datos)
        secuencia.append((i, actual, evento))
        anterior = actual.encode()
    return secuencia


def verificar_tramo(estado_previo, tramo):
    anterior = estado_previo.encode()
    for indice, esperado, evento in tramo:
        datos = anterior if evento is None else anterior + evento.encode()
        actual = hash_sha256(datos)
        if actual != esperado:
            return indice, False
        anterior = actual.encode()
    return tramo[-1][0], True


def verificar_secuencia(semilla, secuencia, numero_tramos):
    n = len(secuencia)
    tamano = -(-n // numero_tramos)
    tramos = [secuencia[i:i + tamano] for i in range(0, n, tamano)]
    resultados = []
    for tramo in tramos:
        primero = tramo[0][0]
        estado_previo = semilla if primero == 1 else secuencia[primero - 2][1]
        resultados.append((tramo, verificar_tramo(estado_previo, tramo)))
    return resultados


def escalado_horizontal(semilla_a, semilla_b, n, cada):
    estado_a, estado_b = semilla_a, semilla_b
    traza = []
    for i in range(1, n + 1):
        estado_a = hash_sha256(estado_a.encode())
        estado_b = hash_sha256(estado_b.encode())
        if i % cada == 0:
            estado_a = estado_b = hash_sha256((estado_a + estado_b).encode())
            traza.append((i, estado_a, True))
        else:
            traza.append((i, estado_a, False))
    return traza


def demo():
    titulo("1. RELOJ SECUENCIAL (hashing encadenado)")
    print("Cada hash depende del anterior: H_i = SHA-256(H_(i-1))")
    print("No hay atajo: para llegar al indice N hay que calcular los N anteriores.\n")
    secuencia = generar_secuencia("semilla-inicial", MUESTRA)
    for indice, h, _ in secuencia:
        nota = "" if indice == 1 else "  <= SHA-256(hash anterior)"
        print(f"  indice {indice:2d} -> {h[:24]}...{nota}")
    print(f"\n  Ultimo hash en indice {MUESTRA}. Cambiar la semilla cambia TODA la secuencia.")

    titulo("2. INSERCION DE EVENTOS EN EL RELOJ")
    print("Un evento E se sella mezclandolo: H = SHA-256(H_previo + E)")
    print("Asi E queda demostradamente despues del hash previo y antes del siguiente.\n")
    eventos = {3: "tx:Manolo->Paco:5", 6: "tx:Eusebio->Manolo:2"}
    secuencia_ev = insertar_eventos("semilla-inicial", MUESTRA, eventos)
    for indice, h, evento in secuencia_ev:
        marca = f"   <-- evento: {evento}" if evento else ""
        print(f"  indice {indice:2d} -> {h[:24]}...{marca}")

    print("\n  Alteramos el evento del indice 3: 'Manolo->Paco:5' pasa a 'Manolo->Paco:50'")
    eventos_alt = {3: "tx:Manolo->Paco:50", 6: "tx:Eusebio->Manolo:2"}
    secuencia_alt = insertar_eventos("semilla-inicial", MUESTRA, eventos_alt)
    for (i, h, _), (_, h_alt, _) in zip(secuencia_ev, secuencia_alt):
        print(f"  indice {i:2d} -> {'IGUAL ' if h == h_alt else 'CAMBIA'}")

    titulo("3. VERIFICACION POR TRAMOS")
    print("Generar es secuencial, pero verificar se reparte en tramos independientes")
    print("(cada tramo va de un hash conocido al siguiente).\n")
    print("Secuencia correcta, 3 tramos:")
    for tramo, (indice, ok) in verificar_secuencia("semilla-inicial", secuencia_ev, 3):
        rango = f"{tramo[0][0]}..{tramo[-1][0]}"
        estado = "OK" if ok else f"FALLO en indice {indice}"
        print(f"  tramo [{rango:>5}] -> {estado}")

    print("\nAhora manipulamos el hash del indice 4:")
    secuencia_tamper = list(secuencia_ev)
    i4, _, e4 = secuencia_tamper[3]
    secuencia_tamper[3] = (i4, "0" * 64, e4)
    for tramo, (indice, ok) in verificar_secuencia("semilla-inicial", secuencia_tamper, 3):
        rango = f"{tramo[0][0]}..{tramo[-1][0]}"
        estado = "OK" if ok else f"FALLO en indice {indice}"
        print(f"  tramo [{rango:>5}] -> {estado}")

    titulo("4. ESCALADO HORIZONTAL")
    print("Dos generadores se sincronizan cruzando sus estados cada ciertos hashes.")
    print("Tras cada cruce, la secuencia de uno depende tambien de la del otro.\n")
    for i, h, cruce in escalado_horizontal("gen-A", "gen-B", 6, 3):
        marca = "   <-- cruce de estados A+B" if cruce else ""
        print(f"  indice {i:2d} -> {h[:24]}...{marca}")


if __name__ == "__main__":
    demo()
