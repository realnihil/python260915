# -*- coding: utf-8 -*-
"""
대한민국 출생아수 및 합계출산율 데이터 클렌징, 다각도 분석 및 시각화 스크립트
- 원본 파일: 출생아수__합계출산율__자연증가_등_20240726084835.xlsx
- 분석 도구: Python, pandas, matplotlib, seaborn
"""

import os
import sys
import re
import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Windows 터미널 출력 인코딩 설정
if sys.platform.startswith('win'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==========================================
# 0. 한글 폰트 및 시각화 기본 설정
# ==========================================
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
sns.set_theme(style="whitegrid", font="Malgun Gothic")
plt.rcParams['axes.unicode_minus'] = False

# ==========================================
# 1. 데이터 로드 및 클렌징 (Data Cleansing)
# ==========================================
def load_and_clean_data(file_path: str) -> pd.DataFrame:
    print("=" * 70)
    print(" [1] 데이터 로드 및 클렌징 (Data Cleansing)")
    print("=" * 70)
    
    # 1) 엑셀 파일 로드 (데이터 시트)
    df_raw = pd.read_excel(file_path, sheet_name='데이터')
    print(f"* 원본 데이터 Shape: {df_raw.shape}")
    
    # 2) 전치 (Transpose): 지표를 열로, 연도를 행으로 변환
    df = df_raw.set_index('기본항목별').T
    
    # 3) 인덱스(연도) 클렌징: '2023 p)' 등 특수문자 제거 후 정수형 변환
    df.index = df.index.astype(str).str.extract(r'(\d{4})')[0].astype(int)
    df.index.name = '연도'
    
    # 4) 컬럼명 정제: 괄호 단위 제거 및 간결화
    # 원본: ['출생아수(명)', '자연증가건수(명)', '조출생률(천명당)', '자연증가율(천명당)', '합계출산율(명)', '출생성비(명)']
    rename_cols = {
        col: col.split('(')[0].strip() for col in df.columns
    }
    df = df.rename(columns=rename_cols)
    
    # 5) 결측치 확인 및 데이터 타입 변환
    # 건수/인원수는 정수형(int64), 비율/율은 실수형(float64)
    type_dict = {
        '출생아수': 'int64',
        '자연증가건수': 'int64',
        '조출생률': 'float64',
        '자연증가율': 'float64',
        '합계출산율': 'float64',
        '출생성비': 'float64'
    }
    df = df.astype(type_dict)
    
    # 6) 파생변수 생성
    # - 출생아수 (만 명 단위)
    df['출생아수_만명'] = df['출생아수'] / 10000.0
    # - 전년 대비 출생아수 증감률 (%)
    df['출생아수_증감률'] = df['출생아수'].pct_change() * 100.0
    # - 연대 구분 (1970년대, 1980년대 ...)
    df['연대'] = (df.index // 10 * 10).astype(str) + '년대'
    
    print("* 클렌징 완료 데이터 정보:")
    print(df.info())
    print("\n* 데이터 첫 5개년:")
    print(df[['출생아수', '자연증가건수', '조출생률', '자연증가율', '합계출산율', '출생성비']].head())
    print("\n* 데이터 최근 5개년:")
    print(df[['출생아수', '자연증가건수', '조출생률', '자연증가율', '합계출산율', '출생성비']].tail())
    
    # 7) 클렌징된 파일 저장
    csv_path = 'cleaned_birth_data.csv'
    xlsx_path = 'cleaned_birth_data.xlsx'
    df.to_csv(csv_path, encoding='utf-8-sig')
    df.to_excel(xlsx_path)
    print(f"\n* 정제 데이터 저장 완료: '{csv_path}', '{xlsx_path}'")
    
    return df

# ==========================================
# 2. 다각도 분석 (Multi-angle Analysis)
# ==========================================
def analyze_data(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print(" [2] pandas 다각도 통계 분석 (Multi-angle Analysis)")
    print("=" * 70)
    
    # (1) 전체 기간 기초 기술통계
    print("\n--- (1) 주요 지표 기초 통계량 (1970 ~ 2023) ---")
    stats = df[['출생아수', '합계출산율', '자연증가건수', '조출생률', '출생성비']].describe()
    print(stats.round(2))
    
    # (2) 1970년 vs 2023년 비교 분석
    y1970 = df.loc[1970]
    y2023 = df.loc[2023]
    
    print("\n--- (2) 1970년 vs 2023년 반세기 변화 비교 ---")
    diff_birth = y2023['출생아수'] - y1970['출생아수']
    pct_birth = (diff_birth / y1970['출생아수']) * 100
    diff_tfr = y2023['합계출산율'] - y1970['합계출산율']
    pct_tfr = (diff_tfr / y1970['합계출산율']) * 100
    
    print(f"- 출생아 수: {y1970['출생아수']:,}명 (1970) -> {y2023['출생아수']:,}명 (2023)")
    print(f"  └ 증감: {diff_birth:,}명 ({pct_birth:.2f}% 감소)")
    print(f"- 합계출산율: {y1970['합계출산율']:.2f}명 (1970) -> {y2023['합계출산율']:.3f}명 (2023)")
    print(f"  └ 증감: {diff_tfr:.3f}명 ({pct_tfr:.2f}% 감소)")
    print(f"- 조출생률(1천명당): {y1970['조출생률']:.1f}명 -> {y2023['조출생률']:.1f}명")
    print(f"- 자연증가건수: +{y1970['자연증가건수']:,}명 -> {y2023['자연증가건수']:,}명 (순감소)")

    # (3) 10년 단위(연대별) 추이 분석
    print("\n--- (3) 연대별(10년 단위) 평균 지표 분석 ---")
    decade_group = df.groupby('연대')[['출생아수', '합계출산율', '자연증가건수', '조출생률', '출생성비']].agg({
        '출생아수': 'mean',
        '합계출산율': 'mean',
        '자연증가건수': 'mean',
        '조출생률': 'mean',
        '출생성비': 'mean'
    }).round(2)
    print(decade_group)
    
    # (4) 인구학적 주요 마일스톤 및 변곡점 도출
    print("\n--- (4) 인구학적 주요 변곡점 및 마일스톤 ---")
    max_birth_yr = df['출생아수'].idxmax()
    min_birth_yr = df['출생아수'].idxmin()
    print(f"- 역대 최대 출생아수 연도: {max_birth_yr}년 ({df.loc[max_birth_yr, '출생아수']:,}명)")
    print(f"- 역대 최저 출생아수 연도: {min_birth_yr}년 ({df.loc[min_birth_yr, '출생아수']:,}명)")
    
    # 인구 대체출산율(2.1명) 첫 붕괴
    below_2_1 = df[df['합계출산율'] < 2.1]
    if not below_2_1.empty:
        first_below_2_1 = below_2_1.index[0]
        print(f"- 인구대체수준(2.1명) 최초 붕괴: {first_below_2_1}년 ({df.loc[first_below_2_1, '합계출산율']:.2f}명)")
    
    # 초저출산 기준(1.3명) 첫 진입
    below_1_3 = df[df['합계출산율'] < 1.3]
    if not below_1_3.empty:
        first_below_1_3 = below_1_3.index[0]
        print(f"- 초저출산사회(1.3명 미만) 최초 진입: {first_below_1_3}년 ({df.loc[first_below_1_3, '합계출산율']:.3f}명)")
    
    # 1.0명 최초 붕괴
    below_1_0 = df[df['합계출산율'] < 1.0]
    if not below_1_0.empty:
        first_below_1_0 = below_1_0.index[0]
        print(f"- 합계출산율 1.0명 최초 붕괴: {first_below_1_0}년 ({df.loc[first_below_1_0, '합계출산율']:.3f}명)")
    
    # 인구 데드크로스(자연감소 전환)
    natural_decrease = df[df['자연증가건수'] < 0]
    if not natural_decrease.empty:
        first_nat_dec = natural_decrease.index[0]
        print(f"- 인구 자연감소(데드크로스) 최초 발생: {first_nat_dec}년 (자연증가건수: {df.loc[first_nat_dec, '자연증가건수']:,}명)")
        
    # 출생성비 불균형 최고치
    max_sex_ratio_yr = df['출생성비'].idxmax()
    print(f"- 출생성비(남아선호) 최고 기록 연도: {max_sex_ratio_yr}년 ({df.loc[max_sex_ratio_yr, '출생성비']:.1f}명, 여아 100명당 남아수)")

    # (5) 전년 대비 출생아수 급감 폭이 컸던 TOP 5 연도
    print("\n--- (5) 전년 대비 출생아수 급감 TOP 5 연도 ---")
    top_drops = df.sort_values(by='출생아수_증감률').head(5)[['출생아수', '출생아수_증감률', '합계출산율']]
    print(top_drops.round(2))
    
    # (6) 주요 지표 간 상관계수 분석
    print("\n--- (6) 주요 지표 간 피어슨 상관계수 행렬 ---")
    corr = df[['출생아수', '합계출산율', '자연증가건수', '조출생률', '출생성비']].corr().round(3)
    print(corr)
    
    return {
        'stats': stats,
        'decade_group': decade_group,
        'top_drops': top_drops,
        'corr': corr
    }

# ==========================================
# 3. 시각화 (Visualization)
# ==========================================
def create_visualizations(df: pd.DataFrame):
    print("\n" + "=" * 70)
    print(" [3] 시각화 차트 생성 (Visualizations)")
    print("=" * 70)
    
    # ----------------------------------------------------
    # [차트 1] 메인 그래프: 연도별 출생아수 추이 라인 그래프
    # ----------------------------------------------------
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    
    # 라인 및 마커 플롯
    ax.plot(df.index, df['출생아수_만명'], color='#1f77b4', linewidth=2.8, 
            marker='o', markersize=5, markerfacecolor='white', markeredgewidth=1.8, markeredgecolor='#1f77b4', 
            label='연간 출생아 수')
    
    # 기준선 (100만 명, 70만 명, 50만 명, 30만 명)
    milestones = [100, 70, 50, 30]
    colors = ['#d62728', '#ff7f0e', '#2ca02c', '#9467bd']
    for m, c in zip(milestones, colors):
        ax.axhline(m, color=c, linestyle='--', linewidth=1.0, alpha=0.6)
        ax.text(1973.5, m + 1.2, f'--- {m}만 명 선 ---', color=c, fontsize=9.5, fontweight='bold', alpha=0.8)
    
    # 주요 마일스톤 주석 (Annotation)
    annotations = [
        (1971, df.loc[1971, '출생아수_만명'], '1971년 정점\n(102.5만 명)', (1973, 108)),
        (1983, df.loc[1983, '출생아수_만명'], '1983년 2.1명 붕괴\n(76.9만 명)', (1983, 86)),
        (2002, df.loc[2002, '출생아수_만명'], '2002년 50만 붕괴\n(49.7만 명, 초저출산)', (1998, 38)),
        (2017, df.loc[2017, '출생아수_만명'], '2017년 40만 붕괴\n(35.8만 명)', (2010, 24)),
        (2020, df.loc[2020, '출생아수_만명'], '2020년 30만 붕괴\n& 데드크로스(27.2만)', (2014, 12)),
        (2023, df.loc[2023, '출생아수_만명'], '2023년 최저\n(23.0만 명)', (2020, 32))
    ]
    
    for yr, val, text, xytext in annotations:
        ax.annotate(text, xy=(yr, val), xytext=xytext,
                    arrowprops=dict(arrowstyle="->", color='#333333', lw=1.2),
                    fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.4", fc="#ffffdd", ec="#888888", lw=1.0, alpha=0.9))
    
    # 2020년 이후 인구감소 구간 음영 처리
    ax.axvspan(2020, 2023, color='red', alpha=0.08, label='인구 자연감소(데드크로스) 구간')
    
    # 그래프 꾸미기
    ax.set_title('대한민국 연도별 출생아 수 추이 (1970 ~ 2023)', fontsize=18, fontweight='bold', pad=18)
    ax.set_xlabel('연도 (Year)', fontsize=13, labelpad=10)
    ax.set_ylabel('출생아 수 (단위: 만 명)', fontsize=13, labelpad=10)
    ax.set_xlim(1968, 2025)
    ax.set_ylim(0, 115)
    
    # x축 눈금 5년 단위
    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
    
    # y축 포맷터 (만 명)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x)}만'))
    
    ax.legend(loc='upper right', fontsize=11, frameon=True)
    plt.tight_layout()
    
    chart1_filename = 'birth_trend_line_chart.png'
    plt.savefig(chart1_filename, dpi=300)
    plt.close()
    print(f"* [차트 1] 연도별 출생아수 라인 그래프 생성 완료: '{chart1_filename}'")
    
    # ----------------------------------------------------
    # [차트 2] 다각도 종합 분석 대시보드 (2x2 서브플롯)
    # ----------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(18, 13), dpi=300)
    
    # Subplot (1): 출생아수 & 합계출산율 이중 축 시계열 (Twin-X)
    ax1 = axes[0, 0]
    ax1_twin = ax1.twinx()
    
    l1 = ax1.plot(df.index, df['출생아수_만명'], color='#1f77b4', lw=2.2, label='출생아수 (만 명)')
    l2 = ax1_twin.plot(df.index, df['합계출산율'], color='#e377c2', lw=2.2, linestyle='--', label='합계출산율 (명)')
    
    # 대체출산율(2.1) & 초저출산(1.3) 선
    ax1_twin.axhline(2.1, color='gray', linestyle=':', alpha=0.7)
    ax1_twin.text(1971, 2.15, '대체출산율 (2.1명)', color='gray', fontsize=8.5)
    ax1_twin.axhline(1.3, color='crimson', linestyle=':', alpha=0.7)
    ax1_twin.text(1971, 1.35, '초저출산 기준 (1.3명)', color='crimson', fontsize=8.5)
    
    ax1.set_title('(1) 출생아수 vs 합계출산율 시계열 추이', fontsize=14, fontweight='bold')
    ax1.set_xlabel('연도')
    ax1.set_ylabel('출생아수 (만 명)', color='#1f77b4')
    ax1_twin.set_ylabel('합계출산율 (가임여성 1인당 명)', color='#e377c2')
    ax1.set_ylim(0, 115)
    ax1_twin.set_ylim(0, 5.0)
    
    lines = l1 + l2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper right')
    
    # Subplot (2): 자연증가건수 (인구 자연증감, 데드크로스)
    ax2 = axes[0, 1]
    nat_inc_man = df['자연증가건수'] / 10000.0
    colors_nat = ['#2ca02c' if v >= 0 else '#d62728' for v in nat_inc_man]
    ax2.bar(df.index, nat_inc_man, color=colors_nat, width=0.8, alpha=0.8)
    ax2.axhline(0, color='black', linewidth=1.2)
    ax2.set_title('(2) 연도별 인구 자연증가건수 (출생 - 사망)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('연도')
    ax2.set_ylabel('자연증가건수 (단위: 만 명)')
    ax2.annotate('2020년 자연감소 전환\n(인구 데드크로스)', xy=(2020, -3.2), xytext=(2003, -12),
                 arrowprops=dict(arrowstyle="->", color='darkred', lw=1.5),
                 fontweight='bold', color='darkred',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#ffe6e6", ec="red", lw=1.0))
    
    # Subplot (3): 연대별(10년 단위) 평균 출생아수 및 합계출산율
    ax3 = axes[1, 0]
    decade_df = df.groupby('연대')[['출생아수_만명', '합계출산율']].mean()
    x_idx = np.arange(len(decade_df.index))
    width = 0.38
    
    b1 = ax3.bar(x_idx - width/2, decade_df['출생아수_만명'], width, label='평균 출생아수 (만 명)', color='#3b528b')
    ax3_twin = ax3.twinx()
    b2 = ax3_twin.bar(x_idx + width/2, decade_df['합계출산율'], width, label='평균 합계출산율 (명)', color='#5ec962')
    
    ax3.set_xticks(x_idx)
    ax3.set_xticklabels(decade_df.index)
    ax3.set_title('(3) 연대별(10년 단위) 평균 지표 비교', fontsize=14, fontweight='bold')
    ax3.set_ylabel('평균 출생아수 (만 명)', color='#3b528b')
    ax3.set_ylim(0, 110)
    ax3_twin.set_ylabel('평균 합계출산율 (명)', color='#2e7d32')
    ax3_twin.set_ylim(0, 5.0)
    
    # 막대 위 수치 레이블 추가
    for bar in b1:
        yval = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2.0, yval + 1.5, f'{yval:.1f}만', ha='center', va='bottom', fontsize=8)
    for bar in b2:
        yval = bar.get_height()
        ax3_twin.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, f'{yval:.2f}', ha='center', va='bottom', fontsize=8)
        
    ax3.legend(loc='upper left')
    ax3_twin.legend(loc='upper right')
    
    # Subplot (4): 출생성비 추이 (여아 100명당 남아 수)
    ax4 = axes[1, 1]
    ax4.plot(df.index, df['출생성비'], color='#ff7f0e', lw=2.2, marker='s', markersize=4)
    # 정상 성비 범위 (103~107) 음영
    ax4.axhspan(103, 107, color='green', alpha=0.15, label='자연 정상 성비 범위 (103~107)')
    ax4.annotate('1990년 최고치 (116.5)\n(남아선호사상 절정)', xy=(1990, 116.5), xytext=(1975, 117),
                 arrowprops=dict(arrowstyle="->", color='#d62728', lw=1.2),
                 fontweight='bold', color='#d62728',
                 bbox=dict(boxstyle="round,pad=0.3", fc="#fff2e6", ec="#ff7f0e", lw=1.0))
    ax4.set_title('(4) 출생성비 변화 추이 (여아 100명당 남아 수)', fontsize=14, fontweight='bold')
    ax4.set_xlabel('연도')
    ax4.set_ylabel('출생성비 (명)')
    ax4.set_ylim(100, 120)
    ax4.legend(loc='lower left')
    
    plt.tight_layout()
    chart2_filename = 'demographic_comprehensive_charts.png'
    plt.savefig(chart2_filename, dpi=300)
    plt.close()
    print(f"* [차트 2] 다각도 종합 분석 대시보드 생성 완료: '{chart2_filename}'")

# ==========================================
# 메인 실행부
# ==========================================
if __name__ == '__main__':
    data_file = '출생아수__합계출산율__자연증가_등_20240726084835.xlsx'
    
    if not os.path.exists(data_file):
        print(f"오류: 데이터 파일 '{data_file}'을 찾을 수 없습니다.")
        sys.exit(1)
        
    # 1. 데이터 클렌징
    df_clean = load_and_clean_data(data_file)
    
    # 2. 다각도 분석
    analysis_results = analyze_data(df_clean)
    
    # 3. 시각화 그래프 생성
    create_visualizations(df_clean)
    
    print("\n" + "=" * 70)
    print(" [완료] 데이터 클렌징, 다각도 분석 및 시각화 작업이 성공적으로 완료되었습니다!")
    print("=" * 70)
