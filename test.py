from invest_simulator import InvestSimulator


k = InvestSimulator.vytvor_data_exponencialni(30)
k = InvestSimulator(k, 1200)
p = InvestSimulator.vytvor_data_linearni(30)
p = InvestSimulator(p, 1200)

k.simul(True)
p.simul(True)
print("exponencialni:", k.hodnota)
print("linearni:", p.hodnota)
print("-"*20)

data = InvestSimulator.vytvor_data_csv("data.csv", "%m/%d/%Y")

k = InvestSimulator(data, 1200)
p = InvestSimulator(data, 1200)
for i in range(1, 13):
    k.pridej_automaticky_nakup(i)
p.pridej_automaticky_nakup(10)
k.simul()
p.simul()

print("nakup kazdy mesic:", k.hodnota)
print("nakup pouze kazdy rijen:", p.hodnota)
print("-"*20)


for i in range(1, 13):
    sim = InvestSimulator(data, 1200)
    sim.pridej_automaticky_nakup(i)
    sim.simul()
    print("mesic:", i, sim.hodnota)
print("-"*20)

for i in [5, 2, 1, 0.7, 0.5, 0.3, 0.2, 0.1, 0.0000001]:
    k = InvestSimulator(data, 1200, zlomek=False, koef_ceny=i)
    k.simul(True)
    print("koef:", i, k.hodnota)
print("-"*20)
