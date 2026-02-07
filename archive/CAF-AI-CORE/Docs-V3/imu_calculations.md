Ciao John,
this is the procedure:
IMU is not applied to your first home . It is applied to other all.

0. Search for Rendita catastale and Categoria catastale of your adpartment (from Catasto)
1. Calculate Rendita catastale rivalutata = Rendita catastale * 1.05  # (rivalutata del 5%)
2. Search for: Coefficiente catastale (è a livello nazionale):
        Function of categoria catastale dell'immobile. Example:
                Categoria catastale               Coefficiente catastale
                 Abitazioni (A, escluso A10):   160
                 Uffici (A10):                              80
                 Negozi (C1):                             55
                 Altri immobili (D):                      65
2  Calculate Base imponibile = Rendita catastale rivalutata × Coefficiente catastale
3  Search for aliquota IMU defined  by Comune  (search data in your comune)
4  Search for IMU discount. Depend for example, if your flat is rent with special contract defined by comune (canone concordato) or several  other cases defined by comune you can have a discount.

Now you are ready to calculate the first data of IMU
IMU=(Base imponibile * Aliquota * Percentuale di possesso/100 * Giorni di possesso/365) * (100-Discout)/100
Esempio pratico:
Supponiamo che tu abbia un immobile con:
Rendita catastale: €1.000
Coefficiente: 160
Aliquota IMU: 0,76%
Percentuale di possesso: 50%
Giorni di possesso: 183 (6 mesi)
Sconto canone concordato = 25%
Calcolo:
Base imponibile = €1.000 × 1,05 × 160 = €168.000
IMU = €168.000 × 0,76/100 × 50/100 × 183/365 × (100-25)/100 =  €240,05


I believe this formula is complete.
Of course in the simplest case the formula become:

Supponiamo che tu abbia un immobile con:
Rendita catastale: €1.000
Coefficiente: 160
Aliquota IMU: 0,76%
Percentuale di possesso: 100%
Giorni di possesso: 365
Sconto canone concordato = 0%
IMU = €168.000 × 0,76/100 × 100/100 × 365/365 × (100-0)/100 =  €1276,8

Now I am studing use case. I will send you asap.

Paolo Meliga

--------------------------------------------------------------------------------------
Ciao John, how are you?
I made a mistake on imu formula!
I understand that imu is monthly
Tax. So to calculate the time of possession it is necessary know the dates.

The IMU must be paid for the months of possession, the month of the sale is charged to those who have had possession for more than 15 days.
Here are some examples:
– deed signed on 4 April: the seller pays for 3 months, the buyer pays for 9 months;
– deed signed on 17 October: the seller pays for 10 months, the buyer for 2 months;
– deed signed on 15 May (31-day month):
Seller pays for 4 months, buyer for 8 months
– deed stipulated on 15 November (30 days): the month of November, equal days of possession between the contracting parties, is imputed by law to the buyer who will pay for 2 months, the seller will pay for 10 months

Italian laws are ... Crazy?
I am waiting for use cases from my friend commercialista.


Attacched IMU role.


Preliminary use case:

New Formula: Mesi di possesso/12
Mesi di possesso: the month of the sale is charged to those who have had possession for more than 15 days.

IMU=(Base imponibile * Aliquota * Percentuale di possesso/100 * Mesi di possesso/12) * (100-Discout)/100

Use case will arrive
