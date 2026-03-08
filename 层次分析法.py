#层次分析法（Analytic Hierarchy Process，AHP）是一种将复杂多目标决策问题结构化、
#量化的方法，核心是把决策目标拆解为 “目标层→准则层→方案层” 的层次结构，
#通过两两比较确定各因素的权重，最终计算方案的综合得分，选出最优解。

#避免主观打分矛盾（比如 “A 比 B 重要，B 比 C 重要，却得出 C 比 A 重要”），核心指标是一致性比率 CR：
#若 CR < 0.1，判断矩阵符合一致性；
#若 CR ≥ 0.1，需重新调整判断矩阵。

import numpy as np
import pandas as pd

class AHP:
    def __init__(self):
        self.CI = 0.0  # 一致性指标
        self.CR = 0.0  # 一致性比率
        self.RI = [0, 0, 0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45]  # 平均随机一致性指标（n=1-9）

    def cal_weight(self,matrix):
        n = matrix.shape[0]
        eigvals, eigvecs = np.linalg.eig(matrix)
        max_eigval=np.max(eigvals)
        max_eigvec = eigvecs[:, np.argmax(eigvals)].real  # 取实部（避免虚数）

        weights=max_eigvec/np.sum(max_eigvec)

        self.CI=(max_eigval-n)/(n-1)

        if n==1:
            self.CR = 0.0
            return weights, True

        self.CR=self.CI/self.RI[n-1]
        return weights,self.CR<0.1
            
    def ahp_calculate(self,criteria_matrix, scheme_matrices):
        criteria_weights, criteria_consistent = self.cal_weight(criteria_matrix)
        if not criteria_consistent:
            print("判断矩阵不一致，请重新调整")
            return None,None
        
        scheme_weights = []
        for i, mat in enumerate(scheme_matrices):
            w, consistent = self.cal_weight(mat)
            scheme_weights.append(w)
            print(f"准则{i+1}下方案层一致性比率 CR = {self.CR:.4f}")
            if not consistent:
                print(f"⚠️ 准则{i+1}下方案层判断矩阵不一致，请重新调整！")
                return None, None
        
        # 3. 计算方案综合得分（加权求和）
        scheme_weights = np.array(scheme_weights).T  # 转置：行=方案，列=准则
        final_scores = np.dot(scheme_weights, criteria_weights)
        
        return final_scores, criteria_weights

# ---------------------- 示例：选最优旅游目的地 ----------------------
if __name__ == "__main__":
    # 1. 构造判断矩阵
    # 准则层：[费用, 风景, 交通] 的两两比较矩阵
    criteria_matrix = np.array([
        [1, 1/3, 2],   # 费用 vs 费用=1，费用 vs 风景=1/3，费用 vs 交通=2
        [3, 1, 5],     # 风景 vs 费用=3，风景 vs 风景=1，风景 vs 交通=5
        [1/2, 1/5, 1]  # 交通 vs 费用=1/2，交通 vs 风景=1/5，交通 vs 交通=1
    ])
    
    # 方案层：各准则下 [云南, 海南, 新疆] 的两两比较矩阵
    # 准则1（费用）下的判断矩阵
    scheme1 = np.array([
        [1, 2, 1/3],
        [1/2, 1, 1/5],
        [3, 5, 1]
    ])
    # 准则2（风景）下的判断矩阵
    scheme2 = np.array([
        [1, 1/4, 2],
        [4, 1, 5],
        [1/2, 1/5, 1]
    ])
    # 准则3（交通）下的判断矩阵
    scheme3 = np.array([
        [1, 3, 1/2],
        [1/3, 1, 1/4],
        [2, 4, 1]
    ])
    scheme_matrices = [scheme1, scheme2, scheme3]
    
    # 2. 执行AHP计算
    ahp = AHP()
    final_scores, criteria_weights = ahp.ahp_calculate(criteria_matrix, scheme_matrices)
    
    # 3. 输出结果
    if final_scores is not None:
        schemes = ["云南", "海南", "新疆"]
        criteria = ["费用", "风景", "交通"]
        
        print("\n===== 层次分析法结果 =====")
        print(f"准则层权重（{criteria}）：{np.round(criteria_weights, 4)}")
        
        # 整理结果为DataFrame，更直观
        result_df = pd.DataFrame({
            "方案": schemes,
            "综合得分": np.round(final_scores, 4),
            "排名": np.argsort(np.argsort(-final_scores)) + 1  # 降序排名
        })
        print("\n方案得分与排名：")
        print(result_df.sort_values("综合得分", ascending=False))