import numpy as np
import gymnasium as gym
import pandas as pd
import indicators
import gym_trading_env
import rtg_pg

def stock_data_curation(ticker = "JPM"):
    df_stk_data = pd.read_csv("data/{}.csv".format(ticker), parse_dates=["Date"], index_col="Date")
    df_stk_data.sort_index(inplace=True)
    df_stk_data.dropna(inplace=True)
    df_stk_data.drop_duplicates(inplace=True)

    df_stk_data["feature_close"] = df_stk_data["close"].pct_change()
    df_stk_data["feature_open"] = df_stk_data["open"] / df_stk_data["close"]
    df_stk_data["feature_high"] = df_stk_data["high"] / df_stk_data["close"]
    df_stk_data["feature_low"] = df_stk_data["low"] / df_stk_data["close"]
    df_stk_data["feature_volume"] = df_stk_data["volume"] / df_stk_data["volume"].rolling(7 * 24).max()

    df_stk_data["feature_bb_value"] = indicators.bb_value()
    df_stk_data["feature_momentum"] = indicators.momentum()
    df_stk_data["feature_SMA"] = indicators.SMA()
    df_stk_data["feature_EMA"] = indicators.EMA()
    df_stk_data["feature_MACD"] = indicators.MACD()
    df_stk_data.dropna(inplace=True)

    return df_stk_data

def create_environment(df):
    return gym.make("TradingEnv",
                    name="JBM",
                    df=df,  # Your dataset with your custom features
                    positions=[-1, 0, 1],  # -1 (=SHORT), 0(=OUT), +1 (=LONG)
                    trading_fees=0.01 / 100,  # 0.01% per stock buy / sell (Binance fees)
                    borrow_interest_rate=0.0003 / 100  # 0.0003% per timestep (one timestep = 1h here)
                    )

if __name__ == '__main__':
    the_rtg_pg = rtg_pg.Rtg_Pg(create_environment(stock_data_curation()))
    the_rtg_pg.train()