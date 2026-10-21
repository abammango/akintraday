# akintraday

**AK Trading Journal**: journal trading satu fail (`index.html`) untuk rekod trade MGC (Micro Gold), MNQ (Micro Nasdaq) dan instrument lain.

## Cara guna

1. Buka `index.html` dalam browser (Chrome / Edge / Safari / Firefox). Tak perlu install apa-apa.
   - Atau aktifkan **GitHub Pages** untuk repo ini (Settings → Pages → branch `main`, folder `/`) supaya boleh buka dari mana-mana.
2. Klik **＋ Trade Baru** dan isi:
   - Tarikh & masa entry
   - Instrument: **MGC**, **MNQ** atau *Lain-lain* (isi simbol + nilai USD per 1 point)
   - Position: **Buy / Long** atau **Sell / Short**
   - Kontrak, harga entry, exit, stop loss, take profit, fees
   - **Profit / Loss (USD)**: dikira automatik dari entry/exit (boleh tukar manual)
   - **Result**: Success / Fail / Breakeven (dipilih automatik ikut P/L)
   - **Analisis SEBELUM**: nota + gambar chart sebelum entry
   - **Review SELEPAS**: nota + gambar chart selepas kejadian
   - Pengajaran / nota, dan sama ada anda ikut trading plan
3. Upload gambar dengan klik, seret & lepas, atau **tampal terus (Ctrl+V)** screenshot dari TradingView.

## Kiraan P/L automatik

| Instrument | Nilai 1 point / kontrak | Tick |
|---|---|---|
| MGC (Micro Gold) | $10 | 0.10 = $1.00 |
| MNQ (Micro Nasdaq-100) | $2 | 0.25 = $0.50 |

`P/L = points × nilai point × kontrak − fees` (Buy: exit − entry, Sell: entry − exit)

## Dashboard

Jumlah P/L, win rate, profit factor, purata success/fail, % ikut plan, equity curve, dan pecahan ikut instrument & Buy/Sell. Boleh filter ikut instrument, position, result, julat tarikh dan carian teks.

## Data & backup

- Semua data (termasuk gambar) disimpan **dalam browser anda sahaja** (IndexedDB), tiada server.
- Data terikat pada browser + alamat yang sama. Kalau buka di komputer/telefon lain, data tak ikut.
- Tekan **Backup** selalu untuk download fail `.json` (termasuk gambar). Guna **Restore** untuk pulihkan atau pindah ke peranti lain.
- **CSV** untuk buka dalam Excel / Google Sheets.
- Jangan guna mod incognito; data akan hilang bila tab ditutup.
