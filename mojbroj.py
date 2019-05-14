import random

s_brojevi = (10, 15, 20)
v_brojevi = (25, 50, 75, 100)

brojevi = []
cilj = 0

operacije = ('+', '-', '*', '/')

def izracunaj_postfiks(izraz):
    s = []
    i = 0
    for el in izraz:
        if type(el) is int:
            s.append(el)
        else:
            y = s.pop()
            x = s.pop()
            if el == '+':
                s.append(x + y)
            elif el == '-':
                s.append(x - y)
            elif el == '*':
                s.append(x * y)
            else:
                # Dodati proveru za deljenje nulom i izmeniti postfiksni izraz na mestu i
                try:
                    s.append(x // y)
                except ZeroDivisionError:
                    return (9*9*9*9*20*100 + i)

        i += 1

    return s[0]

def promena_operacije(h, i):
    while True:
        op = random.choice(operacije)
        if op != h.postfiks[i]:
            h.postfiks.pop(i)
            h.postfiks.insert(i, op)
            break

    return True

def promena_broja(h, i):
    if len(h.dostupni) < 1:
        return False

    x = random.choice(h.dostupni)
    x_s = h.postfiks.pop(i)
    h.postfiks.insert(i, x)

    h.dostupni.append(x_s)
    h.potroseni.remove(x_s)

    h.dostupni.remove(x)
    h.potroseni.append(x)

    return True

def umetanje_broja(h, i):
    if len(h.dostupni) < 2:
        return False

    x, y = random.sample(h.dostupni, 2)
    op = '+'
    if x == 1 or y == 1:
        if x != y:
            op = random.choice(operacije[:2])
        else:
            op = '+'
    else:
        if x % y == 0:
            if x != y:
                op = random.choice(operacije)
            else:
                op = random.choice(operacije[:3])
        else:
            op = random.choice(operacije[:3])

    x_s = h.postfiks.pop(i)
    h.postfiks.insert(i, op)
    h.postfiks.insert(i, y)
    h.postfiks.insert(i, x)

    h.dostupni.append(x_s)
    h.potroseni.remove(x_s)

    h.dostupni.remove(x)
    h.potroseni.append(x)
    h.dostupni.remove(y)
    h.potroseni.append(y)

    return True

def umetanje_operacije(h, i):
    if len(h.dostupni) < 1:
        return False

    x = random.choice(h.dostupni)
    op = '+'
    if x == 1:
        op = random.choice(operacije[:2])
    else:
        op = random.choice(operacije)

    h.postfiks.insert(i, op)
    h.postfiks.insert(i, x)

    h.dostupni.remove(x)
    h.potroseni.append(x)

    return True

def dodavanje(h):

    return

class Hromozom():

    def __init__(self, brojevi, cilj, h=None):

        if h is None:
            self.potroseni = []
            self.dostupni = brojevi.copy()
            self.cilj = cilj
            self.postfiks = []

            for x in random.sample(brojevi, 2):
                self.postfiks.append(x)

            for x in self.postfiks:
                self.potroseni.append(x)
                self.dostupni.remove(x)

            op = '+'
            if 1 in self.postfiks:
                if self.postfiks[0] != self.postfiks[1]:
                    op = random.choice(operacije[:2])
                else:
                    op = '+'
            else:
                if self.postfiks[0] % self.postfiks[1] == 0 and self.postfiks[0] != self.postfiks[1]:
                    op = random.choice(operacije)
                else:
                    op = random.choice(operacije[:3])
            self.postfiks.append(op)

            self.fitnes = 0
            self.rezultat = 0
            self.izracunaj()
        else:
            self.potroseni = h.potroseni.copy()
            self.dostupni = h.dostupni.copy()
            self.postfiks = h.postfiks.copy()
            self.fitnes = h.fitnes
            self.rezultat = h.rezultat
            self.cilj = h.cilj

    def izracunaj(self):
        rez = 9*9*9*9*20*100
        while True:
            rez = izracunaj_postfiks(self.postfiks)
            if rez >= 9*9*9*9*20*100:
                i = rez - 9*9*9*9*20*100
                self.postfiks.pop(i)
                op = random.choice(operacije)
                self.postfiks.insert(i, op)
            else:
                break

        self.rezultat = rez
        self.fitnes = abs(self.cilj - self.rezultat)
        return

    def kopija(self):
        return Hromozom(None, None, h=self)

    def __repr__(self):
        s = []
        for el in self.postfiks:
            if type(el) is int:
                s.append(str(el))
            else:
                y = s.pop()
                x = s.pop()
                s.append(f'({x}{el}{y})')

        return f'{s[0]} = {self.rezultat} [{self.fitnes}]' 

    def mutiraj(self):
        n = len(self.postfiks)

        t = 0
        mutiran = False
        while not mutiran:
            i = random.randint(0, n - 1)
            m = random.uniform(0, 1)

            if m < 0.8:
                if type(self.postfiks[i]) is int:
                    m = random.randint(0, 1)
                    if m < 0.8:
                        mutiran = promena_broja(self, i)
                    else:
                        umetanje_broja(self, i)
                else:
                    m = random.randint(0, 1)
                    if m < 0.8:
                        mutiran = promena_operacije(self, i)
                    else:
                        umetanje_operacije(self, i)
                        pass
            else:
                pass

            t += 1
            if t >= 5 and not mutiran:
                return False

        return True

class Populacija():

    def __init__(self, velicina, brojevi, cilj):
        self.velicina = velicina
        self.brojevi = brojevi
        self.cilj = cilj
        self.hromozomi = [Hromozom(self.brojevi, self.cilj) for _ in range(velicina)]
        self.najbolji = min(self.hromozomi, key=lambda h: h.fitnes).kopija()
        self.izracunaj()

    def izracunaj(self):
        for h in self.hromozomi:
            h.izracunaj()
            if h.fitnes < self.najbolji.fitnes:
                self.najbolji = h.kopija()

        return

    def selekcija(self):
        self.hromozomi.sort(key=lambda h: h.fitnes)
        self.hromozomi = self.hromozomi[:self.velicina // 2]
        return

    def mutiraj(self):
        novi = [h.kopija() for h in self.hromozomi]

        for h in novi:
            if not h.mutiraj():
                self.hromozomi.append(Hromozom(self.brojevi, self.cilj))
            else:
                self.hromozomi.append(h)

        return

    def ispisi(self):
        print('\n'.join(map(str, self.hromozomi)))
        return

if __name__ == '__main__':

    brojevi = []
    for _ in range(4):
        brojevi.append(random.randint(1, 9))

    for s in (s_brojevi, v_brojevi):
        brojevi.append(random.choice(s))

    cilj = random.randint(1, 999)
    print(brojevi, cilj)

    p = Populacija(500, brojevi, cilj)
    i = 0
    for i in range(500):
        if p.najbolji.fitnes == 0:
            break

        if p.najbolji.fitnes in p.najbolji.dostupni:
            p.najbolji.postfiks.append(p.najbolji.fitnes)
            if p.najbolji.rezultat + p.najbolji.fitnes == cilj:
                p.najbolji.postfiks.append('+')
            else:
                p.najbolji.postfiks.append('-')

            break

        if cilj % p.najbolji.rezultat == 0 and cilj // p.najbolji.rezultat in p.najbolji.dostupni:
            p.najbolji.postfiks.append(cilj // p.najbolji.rezultat)
            p.najbolji.postfiks.append('*')
            break

        if p.najbolji.rezultat % cilj == 0 and p.najbolji.rezultat // cilj in p.najbolji.dostupni:
            p.najbolji.postfiks.append(p.najbolji.rezultat // cilj)
            p.najbolji.postfiks.append('/')
            break

        p.selekcija()
        p.mutiraj()
        p.izracunaj()

        if (i + 1) % 50 == 0:
            print(f'Generacija {i + 1} - Najbolje resenje: {p.najbolji}.')

    p.najbolji.izracunaj()
    print(f'Najbolje resenje nadjeno nakon {i + 1} generacija: {p.najbolji}.')
