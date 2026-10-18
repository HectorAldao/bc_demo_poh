def hash_falso(x):
    return x + 1


def titulo(texto):
    print("\n" + "=" * 64)
    print(texto)
    print("=" * 64)


def reloj(semilla, n):
    valor = semilla
    traza = [(0, valor)]
    for paso in range(1, n + 1):
        valor = hash_falso(valor)
        traza.append((paso, valor))
    return traza


def reloj_con_eventos(semilla, n, eventos):
    valor = semilla
    traza = [(0, valor, None)]
    for paso in range(1, n + 1):
        evento = eventos.get(paso)
        if evento is None:
            valor = hash_falso(valor)
        else:
            valor = hash_falso(valor + evento)
        traza.append((paso, valor, evento))
    return traza


def verificar(semilla, eventos, publicados):
    valor = semilla
    resultados = []
    for paso in range(1, len(publicados)):
        evento = eventos.get(paso)
        if evento is None:
            valor = hash_falso(valor)
        else:
            valor = hash_falso(valor + evento)
        esperado = publicados[paso][1]
        resultados.append((paso, valor, esperado, valor == esperado))
    return resultados


def enlazar(semilla_a, semilla_b, n, cada):
    a, b = semilla_a, semilla_b
    traza = []
    for paso in range(1, n + 1):
        a = hash_falso(a)
        b = hash_falso(hash_falso(b))
        if paso % cada == 0:
            a = b = hash_falso(a + b)
            traza.append((paso, a, b, True))
        else:
            traza.append((paso, a, b, False))
    return traza


def demo():
    titulo("EL HASH DE JUGUETE")
    print("Para que se vea, usamos un 'hash' tonto a proposito:  hash(x) = x + 1")
    print("No es criptografico, pero imita lo importante: el resultado solo depende")
    print("del anterior y hay que calcularlo paso a paso.")

    titulo("1. EL RELOJ: EL PASO DEL TIEMPO")
    print("Empezamos en 0 y damos 5 pasos. Cada valor es hash del anterior.\n")
    for paso, valor in reloj(0, 5):
        print(f"  paso {paso} -> valor {valor}")
    print("\n  El valor ES la cuenta de pasos: el 5 prueba que pasaron 5 unidades,")
    print("  y para llegar al 5 hay que recorrer 1, 2, 3 y 4 sin saltarse nada.")

    titulo("2. METER UN EVENTO EN EL RELOJ")
    print("Regla: sin evento, valor = hash(valor_anterior)")
    print("       con evento E, valor = hash(valor_anterior + E)")
    print("El mensaje se SUMA a la corriente y la desplaza para siempre.\n")
    eventos = {3: 100}
    traza = reloj_con_eventos(0, 5, eventos)
    for paso, valor, evento in traza:
        marca = f"   <-- evento {evento}" if evento is not None else ""
        print(f"  paso {paso} -> valor {valor}{marca}")
    print("\n  Sin el evento, el paso 3 valdria 3. El mensaje 100 lo empuja +100,")
    print("  y ese empujon viaja a todos los valores siguientes.")

    print("\nAhora cambiamos ese mensaje (100 -> 50) y comparamos:")
    traza_alt = reloj_con_eventos(0, 5, {3: 50})
    for (paso, h1, _), (_, h2, _) in zip(traza, traza_alt):
        estado = "igual" if h1 == h2 else "CAMBIADO"
        print(f"  paso {paso}: con 100 -> {h1:<5}   con 50 -> {h2:<5}   {estado}")
    print("\n  Un solo mensaje distinto descoloca TODO lo que va detras.")
    print("  Por eso un evento no se puede mover ni falsear sin romper la cadena.")

    titulo("3. VERIFICAR: RECALCULAR Y COMPARAR")
    print("Verificar = recalcular la cadena desde el principio y comparar cada valor")
    print("con el que se publico. Si algo se manipulo, deja de cuadrar.\n")
    eventos = {3: 100, 5: 200}
    publicados = reloj_con_eventos(0, 5, eventos)
    print("  Secuencia publicada:")
    for paso, valor, evento in publicados:
        marca = f"   <-- evento {evento}" if evento is not None else ""
        print(f"    paso {paso} -> {valor}{marca}")

    print("\n  Verificacion con los mensajes correctos:")
    for paso, calc, pub, ok in verificar(0, eventos, publicados):
        print(f"    paso {paso}: recalculado {calc:<5} vs publicado {pub:<5} -> {'OK' if ok else 'FALLO'}")

    print("\n  Un atacante reescribe el mensaje del paso 3 (100 -> 999) y deja los valores viejos:")
    eventos_mal = {3: 999, 5: 200}
    for paso, calc, pub, ok in verificar(0, eventos_mal, publicados):
        print(f"    paso {paso}: recalculado {calc:<5} vs publicado {pub:<5} -> {'OK' if ok else 'FALLO'}")
    print("\n  En el paso 3 el recalculo ya no coincide: manipulacion detectada al momento.")

    titulo("4. ENLAZAR DOS CORRIENTES DE HASHES")
    print("Generador A empieza en 10 y avanza +1 por paso.")
    print("Generador B empieza en 20 y avanza +2 por paso.")
    print("Cada 3 pasos cruzan sus estados: valor_mezcla = hash(A + B).\n")
    for paso, a, b, cruce in enlazar(10, 20, 6, 3):
        marca = "   <-- cruce A+B" if cruce else ""
        print(f"  paso {paso}: A = {a:<4} B = {b:<4}{marca}")
    print("\n  Tras un cruce, A y B comparten historia: ninguno avanza ya por su cuenta.")
    print("  Prueba: cambia solo la semilla de B y mira como cambia A tras el cruce.\n")
    for paso, a, b, cruce in enlazar(10, 21, 6, 3):
        marca = "   <-- cruce A+B" if cruce else ""
        print(f"  paso {paso}: A = {a:<4} B = {b:<4}{marca}")
    print("\n  Con B en 20, A valia 40 en el cruce; con B en 21, A vale 41.")
    print("  El valor de A ahora depende tambien de B: las dos corrientes quedan enlazadas.")

    titulo("EN RESUMEN")
    print("  - El reloj: hashes encadenados que marcan el paso del tiempo.")
    print("  - El evento se suma al hash anterior y desplaza toda la cadena posterior.")
    print("  - Verificar es recalcular y comparar: cualquier cambio canta.")
    print("  - Enlazar dos corrientes hace que una dependa de la historia de la otra.")


if __name__ == "__main__":
    demo()
