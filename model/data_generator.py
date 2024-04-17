#  1. Cada cuenta debe tener una transferencia a la anterior para ser conexa.
#  2. Solo un 10% de las transacciones deben ser fraudulentas.
#  3. 25% de las cuentas deben pertenecer a una empresa y el resto a personas.
#  4. 50% de las cuentas seran monetarias el 35% de ahorro y el resto a plazos.
#  4. Las cuentas a plazos no pueden dar dinero solo recibir.
#  6. Una transaccion es fraudulenta si es mayor a 2500 USD.
from faker import Faker
import random as rd
import pandas as pd

columns = ['nombre_empresa', 'nit_empresa', 'direccion_empresa', 'regimen_empresa', 'sector_empresa',
           'telefono_empresa', 'email_empresa', 'representante_legal_empresa', 'fecha_creacion_empresa',
           'nombre_individuo', 'edad_individuo', 'dpi_individuo', 'nit_individuo', 'direccion_individuo',
           'telefono_individuo', 'email_individuo', 'no_cuenta_cuenta', 'saldo_cuenta', 'fecha_apertura_cuenta',
           'divisa_cuenta', 'estado_cuenta', 'limite_retiro_monetaria', 'tasa_interes_ahorro', 'limite_retiro_ahorro',
           'objetivo_ahorro', 'vencimiento_plazo', 'capital_inicial_plazo', 'frecuencia_pago_plazo',
           'tasa_interes_plazo']

columns_transition = ['dpi_titular', 'nit_titular', 'no_cuenta_titular', 'fecha_inicio_titular', 'rol_titular',
                      'estado_titular', 'cuenta_origen_tran', 'cuenta_destino_tran', 'monto_tran', 'fecha_tran',
                      'descripcion_tran', 'ubicacion_tran', 'tipo_tran', 'alerta_tran']

divizas = ["GTQ", "USD"]
tit_roles = ["ADMIN", "VIEWER"]


class DataGenerator:
    def __init__(self, fraud_limit: int, no_of_accounts: int, no_of_companies: int, no_of_persons: int):
        if no_of_persons + no_of_companies >= no_of_accounts:
            raise Exception("La suma del numero de personas y empreesas debe ser menor al numero de cuentas")

        self.no_of_accounts = no_of_accounts
        self.no_of_companies = no_of_companies
        self.no_of_persons = no_of_persons

        self.account_id = 0
        self.empresa_nit = 0
        self.persona_dpi = 0

        self.limite_fraude = fraud_limit
        self.max_amount = (fraud_limit / 90) * 100

        self.cuentas = []
        self.cuentas_trans_out = []
        self.personas = []
        self.empresas = []
        self.columns = columns
        self.index_dict = {column: index for index, column in enumerate(columns)}
        self.index_dict_relations = {column: index for index, column in enumerate(columns_transition)}
        self.faker = Faker()

    def run(self):
        all_rows_nodes = []

        for _ in range(self.no_of_persons):
            all_rows_nodes.append(self.make_persona())

        for _ in range(self.no_of_companies):
            all_rows_nodes.append(self.make_empresa())

        for _ in range(self.no_of_accounts):
            opt = rd.randint(1, 10)

            if opt <= 5:
                all_rows_nodes.append(self.make_cuenta_monetaria())
            elif opt <= 8:
                all_rows_nodes.append(self.make_cuenta_ahorro())
            else:
                all_rows_nodes.append(self.make_cuenta_plazo())

        all_rows_relations = []
        transaction_relations = self.make_transactions()
        titulations_relations = self.make_titulations()

        for i in transaction_relations:
            all_rows_relations.append(i)

        for i in titulations_relations:
            all_rows_relations.append(i)

        df_relations = pd.DataFrame(all_rows_relations, columns=columns_transition)
        df_nodes = pd.DataFrame(all_rows_nodes, columns=columns)

        df_relations.to_csv("relations.csv", index=False)
        df_nodes.to_csv("nodes.csv", index=False)

    def make_cuenta_monetaria(self):
        index_dict = self.index_dict
        account = [None] * len(columns)

        # Llenamos la cuenta
        account[index_dict["no_cuenta_cuenta"]] = self.account_id
        account[index_dict["saldo_cuenta"]] = rd.randint(0, 10000)
        account[index_dict["fecha_apertura_cuenta"]] = self.faker.iso8601()
        account[index_dict["divisa_cuenta"]] = rd.choice(divizas)
        account[index_dict["estado_cuenta"]] = rd.choice([True, False])
        account[index_dict["limite_retiro_monetaria"]] = rd.randint(1000, 10000)

        # Actualizamos variables
        self.cuentas.append(self.account_id)
        self.cuentas_trans_out.append(self.account_id)
        self.account_id += 1

        return account

    def make_cuenta_ahorro(self):
        index_dict = self.index_dict
        account = [None] * len(columns)

        # Llenamos la cuenta
        account[index_dict["no_cuenta_cuenta"]] = self.account_id
        account[index_dict["saldo_cuenta"]] = rd.randint(0, 10000)
        account[index_dict["fecha_apertura_cuenta"]] = self.faker.iso8601()
        account[index_dict["divisa_cuenta"]] = rd.choice(divizas)
        account[index_dict["estado_cuenta"]] = rd.choice([True, False])
        account[index_dict["tasa_interes_ahorro"]] = rd.uniform(0.001, 0.7)
        account[index_dict["limite_retiro_ahorro"]] = rd.randint(1000, 10000)
        account[index_dict["objetivo_ahorro"]] = self.faker.sentence()

        # Actualizamos variables
        self.cuentas.append(self.account_id)
        self.cuentas_trans_out.append(self.account_id)
        self.account_id += 1

        return account

    def make_cuenta_plazo(self):
        index_dict = self.index_dict
        account = [None] * len(columns)

        # Llenamos la cuenta
        account[index_dict["no_cuenta_cuenta"]] = self.account_id
        account[index_dict["saldo_cuenta"]] = rd.randint(0, 10000)
        account[index_dict["fecha_apertura_cuenta"]] = self.faker.iso8601()
        account[index_dict["divisa_cuenta"]] = rd.choice(divizas)
        account[index_dict["estado_cuenta"]] = rd.choice([True, False])
        account[index_dict["vencimiento_plazo"]] = self.faker.iso8601()
        account[index_dict["capital_inicial_plazo"]] = rd.randint(1000, 10000)
        account[index_dict["frecuencia_pago_plazo"]] = self.faker.sentence()
        account[index_dict["tasa_interes_plazo"]] = rd.uniform(0.001, 0.7)

        # Actualizamos variables
        self.cuentas.append(self.account_id)
        self.account_id += 1

        return account

    def make_empresa(self):
        index_dict = self.index_dict
        company = [None] * len(columns)

        # Llenamos la empresa
        company[index_dict["nit_empresa"]] = str(self.empresa_nit)
        company[index_dict["nombre_empresa"]] = self.faker.company()
        company[index_dict["direccion_empresa"]] = self.faker.address()
        company[index_dict["regimen_empresa"]] = self.faker.sentence()
        company[index_dict["sector_empresa"]] = self.faker.sentence()
        company[index_dict["telefono_empresa"]] = self.faker.phone_number()
        company[index_dict["email_empresa"]] = self.faker.email()
        company[index_dict["representante_legal_empresa"]] = self.faker.name()
        company[index_dict["fecha_creacion_empresa"]] = self.faker.iso8601()

        # Actualizamos variables
        self.empresas.append(str(self.empresa_nit))
        self.empresa_nit += 1

        return company

    def make_persona(self):
        index_dict = self.index_dict
        person = [None] * len(columns)

        # Llenamos la persona
        person[index_dict["dpi_individuo"]] = str(self.persona_dpi)
        person[index_dict["nombre_individuo"]] = self.faker.name()
        person[index_dict["edad_individuo"]] = rd.randint(18, 100)
        person[index_dict["nit_individuo"]] = self.faker.ssn()
        person[index_dict["direccion_individuo"]] = self.faker.address()
        person[index_dict["telefono_individuo"]] = self.faker.phone_number()
        person[index_dict["email_individuo"]] = self.faker.email()

        # Actualizamos variables
        self.personas.append(str(self.persona_dpi))
        self.persona_dpi += 1

        return person

    def make_transactions(self):
        relations = []

        for cuenta in self.cuentas_trans_out:
            no_of_transactions = rd.randint(1, 10)

            for _ in range(no_of_transactions):
                transaction = [None] * len(columns_transition)
                transaction[self.index_dict_relations["cuenta_origen_tran"]] = cuenta
                transaction[self.index_dict_relations["cuenta_destino_tran"]] = rd.choice(self.cuentas)
                transaction[self.index_dict_relations["monto_tran"]] = rd.randint(0, int(self.max_amount))
                transaction[self.index_dict_relations["fecha_tran"]] = self.faker.iso8601()
                transaction[self.index_dict_relations["descripcion_tran"]] = self.faker.sentence()
                transaction[self.index_dict_relations["ubicacion_tran"]] = self.faker.address()
                transaction[self.index_dict_relations["tipo_tran"]] = rd.choice(["TRANSFERENCIA", "PAGO", "DEPOSITO"])
                transaction[self.index_dict_relations["alerta_tran"]] = rd.choice(
                    [True, False, False, False, False, False, False, False, False, False])

                relations.append(transaction)

        return relations

    def make_titulations(self):
        # hacemos una primera iteracion sobre las personas y empresas para asegurarnos que todas las personas y empresas
        # tengan al menos una cuenta
        shuffled_accounts = self.cuentas.copy()
        rd.shuffle(shuffled_accounts)
        relations = []

        for person in self.personas:
            relation = [None] * len(columns_transition)
            account = shuffled_accounts.pop()

            relation[self.index_dict_relations["dpi_titular"]] = person
            relation[self.index_dict_relations["no_cuenta_titular"]] = account
            relation[self.index_dict_relations["rol_titular"]] = rd.choice(tit_roles)
            relation[self.index_dict_relations["fecha_inicio_titular"]] = self.faker.iso8601()
            relation[self.index_dict_relations["estado_titular"]] = rd.choice([True, True, True, True, True, False])

            relations.append(relation)

        for company in self.empresas:
            relation = [None] * len(columns_transition)
            account = shuffled_accounts.pop()

            relation[self.index_dict_relations["nit_titular"]] = company
            relation[self.index_dict_relations["no_cuenta_titular"]] = account
            relation[self.index_dict_relations["rol_titular"]] = rd.choice(tit_roles)
            relation[self.index_dict_relations["fecha_inicio_titular"]] = self.faker.iso8601()
            relation[self.index_dict_relations["estado_titular"]] = rd.choice([True, True, True, True, True, False])

        # hacemos una segunda iteracion sobre las personas y empresas para asegurarnos que todas las cuentas tengan
        # al menos una titulacion
        while len(shuffled_accounts) > 0:
            empresas_list = list(self.empresas).copy()
            personas_list = list(self.personas).copy()

            # elegimos si le vamos a asignar la cuenta una persona o empresa
            opt = rd.choice([False, False, False, False, True])

            if opt:
                empresa = rd.choice(empresas_list)
                relation = [None] * len(columns_transition)

                relation[self.index_dict_relations["nit_titular"]] = empresa
                relation[self.index_dict_relations["no_cuenta_titular"]] = shuffled_accounts.pop()
                relation[self.index_dict_relations["rol_titular"]] = rd.choice(tit_roles)
                relation[self.index_dict_relations["fecha_inicio_titular"]] = self.faker.iso8601()
                relation[self.index_dict_relations["estado_titular"]] = rd.choice([True, True, True, True, True, False])

                relations.append(relation)

            else:
                persona = rd.choice(personas_list)
                relation = [None] * len(columns_transition)

                relation[self.index_dict_relations["dpi_titular"]] = persona
                relation[self.index_dict_relations["no_cuenta_titular"]] = shuffled_accounts.pop()
                relation[self.index_dict_relations["rol_titular"]] = rd.choice(tit_roles)
                relation[self.index_dict_relations["fecha_inicio_titular"]] = self.faker.iso8601()
                relation[self.index_dict_relations["estado_titular"]] = rd.choice([True, True, True, True, True, False])

                relations.append(relation)

        return relations
