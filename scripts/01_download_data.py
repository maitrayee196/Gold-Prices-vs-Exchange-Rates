"""Download raw data by shallow-cloning public GitHub dataset mirrors.

Sources (all free, auto-updated mirrors of official series):
  - LBMA gold PM fix (daily, USD/GBP/EUR)  <- unbalancedparentheses/forex-centuries
  - FRED broad dollar index DTWEXBGS       <- unbalancedparentheses/forex-centuries
  - Fed H.10 daily exchange rates          <- datasets/exchange-rates
  - CBOE VIX daily                         <- datasets/finance-vix
  - LBMA gold monthly average              <- datasets/gold-prices

If you prefer primary sources, the same series are available from
LBMA (prices.lbma.org.uk), FRED (fred.stlouisfed.org) and CBOE directly.
"""
import subprocess
import shutil
import tempfile
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)


def clone(url, tmp, sparse_file=None):
    dest = Path(tmp) / url.split("/")[-1]
    if sparse_file:
        subprocess.run(["git", "clone", "--depth", "1", "--filter=blob:none",
                        "--no-checkout", url, str(dest)], check=True)
        subprocess.run(["git", "checkout", "HEAD", "--", sparse_file],
                       cwd=dest, check=True)
    else:
        subprocess.run(["git", "clone", "--depth", "1", url, str(dest)], check=True)
    return dest


with tempfile.TemporaryDirectory() as tmp:
    fc = clone("https://github.com/unbalancedparentheses/forex-centuries", tmp,
               "data/sources/lbma/lbma_gold_daily.csv")
    subprocess.run(["git", "checkout", "HEAD", "--",
                    "data/sources/fred/daily/fred_usd_broad_index.csv"],
                   cwd=fc, check=True)
    shutil.copy(fc / "data/sources/lbma/lbma_gold_daily.csv", RAW)
    shutil.copy(fc / "data/sources/fred/daily/fred_usd_broad_index.csv", RAW)

    er = clone("https://github.com/datasets/exchange-rates", tmp)
    shutil.copy(er / "data/daily.csv", RAW / "h10_fx_daily.csv")

    vx = clone("https://github.com/datasets/finance-vix", tmp)
    shutil.copy(vx / "data/vix-daily.csv", RAW)

    gp = clone("https://github.com/datasets/gold-prices", tmp)
    shutil.copy(gp / "data/monthly.csv", RAW / "lbma_gold_monthly.csv")

print("raw data in", RAW)
for p in sorted(RAW.glob("*.csv")):
    print(" -", p.name)
