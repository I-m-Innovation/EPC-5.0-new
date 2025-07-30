import pandas as pd
from ftplib import FTP

def crea_tabella_leasing(offerta):
    leasing_list = [
        f'{"{0:,.2f}".format(offerta.leasing_primo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                         ",") if offerta.leasing_primo_anno else '€',
        f'{"{0:,.2f}".format(offerta.leasing_secondo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                           ",") if offerta.leasing_secondo_anno else '€',
        f'{"{0:,.2f}".format(offerta.leasing_terzo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                         ",") if offerta.leasing_terzo_anno else '€',
        f'{"{0:,.2f}".format(offerta.leasing_quarto_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                          ",") if offerta.leasing_quarto_anno else '€',
        f'{"{0:,.2f}".format(offerta.leasing_quinto_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                          ",") if offerta.leasing_quinto_anno else '€',
        f'{"{0:,.2f}".format(offerta.leasing_sesto_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                         ",") if offerta.leasing_sesto_anno else '€',
        f'{"{0:,.2f}".format(offerta.leasing_settimo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                           ",") if offerta.leasing_settimo_anno else '€',
        f'{"{0:,.2f}".format(offerta.leasing_ottavo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                          ",") if offerta.leasing_ottavo_anno else '€',
        f'{"{0:,.2f}".format(offerta.leasing_nono_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                        ",") if offerta.leasing_nono_anno else '€',
        f'{"{0:,.2f}".format(offerta.leasing_decimo_anno)} €'.replace(".", ";").replace(",", ".").replace(";",
                                                                                                          ",") if offerta.leasing_decimo_anno else '€',
    ]

    delta_leasing_list = [
        f"{round(offerta.delta_leasing_primo_anno, 2):,} €".replace(".", ";").replace(",", ".").replace(";",
                                                                                                        ",") if offerta.delta_leasing_primo_anno else '€',
        f"{round(offerta.delta_leasing_secondo_anno, 2):,} €".replace(".", ";").replace(",", ".").replace(";",
                                                                                                          ",") if offerta.delta_leasing_secondo_anno else '€',
        f"{round(offerta.delta_leasing_terzo_anno, 2):,} €".replace(".", ";").replace(",", ".").replace(";",
                                                                                                        ",") if offerta.delta_leasing_terzo_anno else '€',
        f"{round(offerta.delta_leasing_quarto_anno, 2):,} €".replace(".", ";").replace(",", ".").replace(";",
                                                                                                         ",") if offerta.delta_leasing_quarto_anno else '€',
        f"{round(offerta.delta_leasing_quinto_anno, 2):,} €".replace(".", ";").replace(",", ".").replace(";",
                                                                                                         ",") if offerta.delta_leasing_quinto_anno else '€',
        f"{round(offerta.delta_leasing_sesto_anno, 2):,} €".replace(".", ";").replace(",", ".").replace(";",
                                                                                                        ",") if offerta.delta_leasing_sesto_anno else '€',
        f"{round(offerta.delta_leasing_settimo_anno, 2):,} €".replace(".", ";").replace(",", ".").replace(";",
                                                                                                          ",") if offerta.delta_leasing_settimo_anno else '€',
        f"{round(offerta.delta_leasing_ottavo_anno, 2):,} €".replace(".", ";").replace(",", ".").replace(";",
                                                                                                         ",") if offerta.delta_leasing_ottavo_anno else '€',
        f"{round(offerta.delta_leasing_nono_anno, 2):,} €".replace(".", ";").replace(",", ".").replace(";",
                                                                                                       ",") if offerta.delta_leasing_nono_anno else '€',
        f"{round(offerta.delta_leasing_decimo_anno, 2):,} €".replace(".", ";").replace(",", ".").replace(";",
                                                                                                         ",") if offerta.delta_leasing_decimo_anno else '€',
    ]
    indexes = [int(number) for number in range(1, 11)]
    index_anno = ['secondo', 'terzo', 'quarto', 'quinto', 'sesto', 'settimo', 'ottavo', 'nono', 'decimo']
    leasing_tab = pd.DataFrame(zip(indexes[1:], index_anno, leasing_list[1:], delta_leasing_list[1:]),
                               columns=["index", "index_anno", "valore", "delta"])

    return leasing_tab


def store_db():
    # ftp = FTP("192.168.10.211", timeout=10)
    print("Salvando db")
    try:
        ftp = FTP("104.167.29.244", timeout=10)        
    except:
        ftp = FTP("192.168.10.211", timeout=10)


    ftp.login('ftpdaticentzilio', 'Sd2PqAS.We8zBK')
    ftp.cwd('/dati/db offerte 5.0')
    file_name = "db.sqlite3"
    file = open(file_name, "rb")
    ftp.storbinary(f"STOR " + file_name, file)
    ftp.close()
    print("Db salvato")

