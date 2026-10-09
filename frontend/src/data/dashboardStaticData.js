/**
 * Dữ liệu Báo cáo Thực nghiệm Đóng Băng (Project 16)
 * Trích xuất nguyên bản từ reports/final_test_evaluation.json, reports/exp1_depth_results.json,
 * reports/exp4_feature_stability_results.json và backend/models/model_metadata.json.
 * Tuyệt đối không tự tính lại Test, không sửa đổi hay bịa đặt giá trị.
 */

export const STATIC_DASHBOARD_DATA = {
  final_test: {
    project_name: "Project 16 - WDBC Classification",
    evaluation_phase: "FINAL_TEST_EVALUATION",
    status: "COMPLETED",
    evaluation_date: "2026-10-09",
    dataset_split: {
      train_samples: 398,
      val_samples: 85,
      test_samples: 86,
      test_benign_count: 54,
      test_malignant_count: 32
    },
    locked_model_config: {
      project_name: "Project 16 - Breast Cancer Wisconsin Diagnostic Classification",
      model_selection: {
        selected_model: "RandomForestClassifier",
        rationale: "Random Forest vượt trội toàn diện so với DummyClassifier và các Cây quyết định đơn lẻ trên cả 5-Fold Cross-Validation và tập Validation độc lập. Mô hình đạt ROC-AUC 0.9941 trên Validation, hạ số ca bỏ sót bệnh (False Negatives) xuống chỉ còn 3 ca (Recall 90.62%), đồng thời không mắc lỗi báo động giả nào (Precision 100.0%, FP=0). Cơ chế tập hợp 100 cây con với Random Feature Selection (max_features=0.3) triệt tiêu phương sai, giải quyết triệt để vấn đề Overfitting của cây đơn lẻ."
      },
      locked_hyperparameters: {
        n_estimators: 100,
        criterion: "gini",
        max_depth: 8,
        min_samples_split: 2,
        min_samples_leaf: 1,
        max_features: 0.3,
        bootstrap: true,
        random_state: 42,
        n_jobs: -1
      },
      target_definition: {
        positive_class: 1,
        positive_label: "Malignant (Ác tính)",
        negative_class: 0,
        negative_label: "Benign (Lành tính)"
      },
      locked_decision_threshold: {
        threshold: 0.5,
        rationale: "Sử dụng ngưỡng xác suất mặc định chuẩn 0.50. Trên tập Validation, ngưỡng 0.50 đã mang lại sự cân bằng hoàn hảo giữa độ nhạy lâm sàng (Recall 90.62%) và độ chuẩn xác tuyệt đối (Precision 100.0%), tránh nguy cơ overfitting ngưỡng phân loại (threshold overfitting)."
      },
      retraining_strategy: {
        evaluation_model: "Model fit on Train (N=398) to provide rigorous, direct benchmarking against Validation (N=85) and Test (N=86).",
        production_model: "Model fit on Train + Validation (N=483) with identical frozen hyperparameters for final deployment."
      },
      leakage_verification: {
        test_set_status: "Strictly frozen (N=86, 54 Benign, 32 Malignant). No preprocessing or hyperparameter search was conducted on Test.",
        verified_at: "2026-10-09"
      }
    },
    test_metrics_summary: {
      accuracy: 0.9884,
      accuracy_95_ci: [0.937, 0.9979],
      precision_malignant: 1.0,
      recall_malignant: 0.9688,
      recall_95_ci: [0.8426, 0.9945],
      f1_malignant: 0.9841,
      roc_auc: 0.9954,
      confusion_matrix: {
        matrix: [[54, 0], [1, 31]],
        tn: 54,
        fp: 0,
        fn: 1,
        tp: 31
      }
    },
    classification_report: {
      Benign: {
        precision: 0.9818,
        recall: 1.0,
        f1_score: 0.9908,
        support: 54
      },
      Malignant: {
        precision: 1.0,
        recall: 0.9688,
        f1_score: 0.9841,
        support: 32
      },
      accuracy: 0.9884,
      macro_avg: {
        precision: 0.9909,
        recall: 0.9844,
        f1_score: 0.9875,
        support: 86
      },
      weighted_avg: {
        precision: 0.9886,
        recall: 0.9884,
        f1_score: 0.9883,
        support: 86
      }
    },
    comparison_with_validation_and_cv: {
      train_accuracy: 1.0,
      cv_mean_recall: 0.9251,
      cv_recall_std: 0.0408,
      val_recall: 0.9062,
      test_recall: 0.9688,
      cv_mean_roc_auc: 0.982,
      val_roc_auc: 0.9941,
      test_roc_auc: 0.9954
    },
    experiment_2_all_models_on_test: {
      DummyClassifier: {
        model_name: "Baseline Dummy (Most Frequent)",
        accuracy: 0.6279,
        recall_malignant: 0.0,
        precision_malignant: 0.0,
        f1_malignant: 0.0,
        roc_auc: 0.5,
        confusion_matrix: { tn: 54, fp: 0, fn: 32, tp: 0 }
      },
      "Unpruned DT": {
        model_name: "Decision Tree (Chưa cắt tỉa)",
        accuracy: 0.907,
        recall_malignant: 0.875,
        precision_malignant: 0.875,
        f1_malignant: 0.875,
        roc_auc: 0.9005,
        confusion_matrix: { tn: 50, fp: 4, fn: 4, tp: 28 }
      },
      "Pruned DT": {
        model_name: "Decision Tree (Cắt tỉa CCP-Alpha)",
        accuracy: 0.9302,
        recall_malignant: 0.8438,
        precision_malignant: 0.9643,
        f1_malignant: 0.9,
        roc_auc: 0.8843,
        confusion_matrix: { tn: 53, fp: 1, fn: 5, tp: 27 }
      },
      "Random Forest": {
        model_name: "Random Forest (Mô hình chọn cuối)",
        accuracy: 0.9884,
        recall_malignant: 0.9688,
        precision_malignant: 1.0,
        f1_malignant: 0.9841,
        roc_auc: 0.9954,
        confusion_matrix: { tn: 54, fp: 0, fn: 1, tp: 31 }
      }
    },
    production_model_on_trainval: {
      total_fit_samples: 483,
      test_roc_auc: 0.9983,
      saved_artifact_path: "backend/models/rf_final.joblib"
    }
  },
  exp1_depth: {
    experiment_name: "Experiment 1: Tree Depth vs Performance",
    dataset: "WDBC Train Set (N=398)",
    cv_method: "5-Fold StratifiedKFold",
    random_state: 42,
    depth_range: [1, 20],
    analysis: {
      recommended_depth: 8,
      recommended_metrics: {
        cv_recall_mean: 0.8984,
        cv_f1_mean: 0.899,
        cv_accuracy_mean: 0.9246
      },
      zones: {
        underfitting_zone: "max_depth = 1 đến 2: Cây quá nông, mô hình đơn giản hóa quá mức, cả Train và CV score đều thấp (< 90%).",
        sweet_spot_zone: "max_depth = 3 đến 8: CV score đạt đỉnh, phương sai thấp, cây giữ độ phức tạp vừa phải.",
        overfitting_zone: "max_depth >= 8: Train score tiệm cận 100% nhưng CV score bão hòa, khoảng cách Train-CV bị nới rộng."
      }
    },
    records: [
      { max_depth: 1, train_accuracy: 0.9315, cv_accuracy_mean: 0.8994, cv_accuracy_std: 0.0254, train_recall_malignant: 0.87, cv_recall_mean: 0.8299, cv_recall_std: 0.0913, train_f1_malignant: 0.9044, cv_f1_mean: 0.8577, cv_f1_std: 0.045 },
      { max_depth: 2, train_accuracy: 0.9579, cv_accuracy_mean: 0.902, cv_accuracy_std: 0.0202, train_recall_malignant: 0.9308, cv_recall_mean: 0.8439, cv_recall_std: 0.0882, train_f1_malignant: 0.9433, cv_f1_mean: 0.8632, cv_f1_std: 0.0346 },
      { max_depth: 3, train_accuracy: 0.9705, cv_accuracy_mean: 0.9221, cv_accuracy_std: 0.0314, train_recall_malignant: 0.9274, cv_recall_mean: 0.8506, cv_recall_std: 0.0832, train_f1_malignant: 0.9589, cv_f1_mean: 0.8892, cv_f1_std: 0.0483 },
      { max_depth: 4, train_accuracy: 0.9843, cv_accuracy_mean: 0.9221, cv_accuracy_std: 0.0314, train_recall_malignant: 0.9679, cv_recall_mean: 0.8713, cv_recall_std: 0.0762, train_f1_malignant: 0.9787, cv_f1_mean: 0.8913, cv_f1_std: 0.0472 },
      { max_depth: 5, train_accuracy: 0.9912, cv_accuracy_mean: 0.917, cv_accuracy_std: 0.0307, train_recall_malignant: 0.9764, cv_recall_mean: 0.8641, cv_recall_std: 0.079, train_f1_malignant: 0.988, cv_f1_mean: 0.884, cv_f1_std: 0.0484 },
      { max_depth: 6, train_accuracy: 0.9956, cv_accuracy_mean: 0.9069, cv_accuracy_std: 0.0346, train_recall_malignant: 0.9882, cv_recall_mean: 0.8572, cv_recall_std: 0.0773, train_f1_malignant: 0.994, cv_f1_mean: 0.8716, cv_f1_std: 0.0508 },
      { max_depth: 7, train_accuracy: 0.9981, cv_accuracy_mean: 0.9221, cv_accuracy_std: 0.027, train_recall_malignant: 0.9941, cv_recall_mean: 0.8844, cv_recall_std: 0.0712, train_f1_malignant: 0.9975, cv_f1_mean: 0.8927, cv_f1_std: 0.0435 },
      { max_depth: 8, train_accuracy: 1.0, cv_accuracy_mean: 0.9246, cv_accuracy_std: 0.0246, train_recall_malignant: 1.0, cv_recall_mean: 0.8984, cv_recall_std: 0.0658, train_f1_malignant: 1.0, cv_f1_mean: 0.899, cv_f1_std: 0.038 },
      { max_depth: 9, train_accuracy: 1.0, cv_accuracy_mean: 0.9195, cv_accuracy_std: 0.0306, train_recall_malignant: 1.0, cv_recall_mean: 0.8915, cv_recall_std: 0.0546, train_f1_malignant: 1.0, cv_f1_mean: 0.8921, cv_f1_std: 0.04 },
      { max_depth: 10, train_accuracy: 1.0, cv_accuracy_mean: 0.9195, cv_accuracy_std: 0.0306, train_recall_malignant: 1.0, cv_recall_mean: 0.8915, cv_recall_std: 0.0546, train_f1_malignant: 1.0, cv_f1_mean: 0.8921, cv_f1_std: 0.04 },
      { max_depth: 12, train_accuracy: 1.0, cv_accuracy_mean: 0.9195, cv_accuracy_std: 0.0306, train_recall_malignant: 1.0, cv_recall_mean: 0.8915, cv_recall_std: 0.0546, train_f1_malignant: 1.0, cv_f1_mean: 0.8921, cv_f1_std: 0.04 },
      { max_depth: 15, train_accuracy: 1.0, cv_accuracy_mean: 0.9195, cv_accuracy_std: 0.0306, train_recall_malignant: 1.0, cv_recall_mean: 0.8915, cv_recall_std: 0.0546, train_f1_malignant: 1.0, cv_f1_mean: 0.8921, cv_f1_std: 0.04 },
      { max_depth: 20, train_accuracy: 1.0, cv_accuracy_mean: 0.9195, cv_accuracy_std: 0.0306, train_recall_malignant: 1.0, cv_recall_mean: 0.8915, cv_recall_std: 0.0546, train_f1_malignant: 1.0, cv_f1_mean: 0.8921, cv_f1_std: 0.04 }
    ]
  },
  exp4_stability: {
    experiment_name: "EXP4_Feature_Importance_Stability",
    model_type: "RandomForestClassifier",
    model_parameters: {
      n_estimators: 100,
      max_depth: 8,
      min_samples_leaf: 1,
      max_features: 0.3
    },
    seeds_evaluated: [42, 123, 456, 789, 999],
    train_samples_count: 398,
    total_features_count: 30,
    top_10_features_summary: [
      {
        feature_name: "perimeter_worst",
        label: "Chu vi tệ nhất",
        mean_importance: 0.182134,
        std_importance: 0.04622,
        cv_pct: 25.38,
        mean_rank: 2.0,
        std_rank: 1.55,
        seed_importances: { seed_42: 0.0964, seed_123: 0.214, seed_456: 0.2131, seed_789: 0.2169, seed_999: 0.1703 }
      },
      {
        feature_name: "radius_worst",
        label: "Bán kính tệ nhất",
        mean_importance: 0.137026,
        std_importance: 0.036363,
        cv_pct: 26.54,
        mean_rank: 3.0,
        std_rank: 1.26,
        seed_importances: { seed_42: 0.1345, seed_123: 0.1225, seed_456: 0.0956, seed_789: 0.1277, seed_999: 0.2048 }
      },
      {
        feature_name: "area_worst",
        label: "Diện tích tệ nhất",
        mean_importance: 0.135639,
        std_importance: 0.039363,
        cv_pct: 29.02,
        mean_rank: 2.8,
        std_rank: 1.47,
        seed_importances: { seed_42: 0.2016, seed_123: 0.1233, seed_456: 0.1516, seed_789: 0.1177, seed_999: 0.084 }
      },
      {
        feature_name: "concave points_mean",
        label: "Điểm lõm trung bình",
        mean_importance: 0.132843,
        std_importance: 0.024139,
        cv_pct: 18.17,
        mean_rank: 3.2,
        std_rank: 0.98,
        seed_importances: { seed_42: 0.1558, seed_123: 0.1125, seed_456: 0.1108, seed_789: 0.168, seed_999: 0.1171 }
      },
      {
        feature_name: "concave points_worst",
        label: "Điểm lõm tệ nhất",
        mean_importance: 0.117032,
        std_importance: 0.02728,
        cv_pct: 23.31,
        mean_rank: 4.0,
        std_rank: 0.89,
        seed_importances: { seed_42: 0.1158, seed_123: 0.1107, seed_456: 0.1283, seed_789: 0.073, seed_999: 0.1572 }
      },
      {
        feature_name: "area_mean",
        label: "Diện tích trung bình",
        mean_importance: 0.038054,
        std_importance: 0.014977,
        cv_pct: 39.36,
        mean_rank: 8.0,
        std_rank: 3.03,
        seed_importances: { seed_42: 0.038, seed_123: 0.0506, seed_456: 0.0361, seed_789: 0.0541, seed_999: 0.0115 }
      },
      {
        feature_name: "perimeter_mean",
        label: "Chu vi trung bình",
        mean_importance: 0.032434,
        std_importance: 0.00715,
        cv_pct: 22.04,
        mean_rank: 7.4,
        std_rank: 1.02,
        seed_importances: { seed_42: 0.0443, seed_123: 0.0316, seed_456: 0.0263, seed_789: 0.0358, seed_999: 0.0243 }
      },
      {
        feature_name: "radius_mean",
        label: "Bán kính trung bình",
        mean_importance: 0.027267,
        std_importance: 0.015132,
        cv_pct: 55.49,
        mean_rank: 9.6,
        std_rank: 3.5,
        seed_importances: { seed_42: 0.0088, seed_123: 0.0181, seed_456: 0.0371, seed_789: 0.0209, seed_999: 0.0514 }
      },
      {
        feature_name: "concavity_mean",
        label: "Độ lõm trung bình",
        mean_importance: 0.026015,
        std_importance: 0.007388,
        cv_pct: 28.4,
        mean_rank: 8.6,
        std_rank: 1.36,
        seed_importances: { seed_42: 0.0293, seed_123: 0.0372, seed_456: 0.028, seed_789: 0.0178, seed_999: 0.0179 }
      },
      {
        feature_name: "symmetry_worst",
        label: "Độ đối xứng tệ nhất",
        mean_importance: 0.019989,
        std_importance: 0.003939,
        cv_pct: 19.71,
        mean_rank: 10.4,
        std_rank: 1.36,
        seed_importances: { seed_42: 0.0151, seed_123: 0.0258, seed_456: 0.0233, seed_789: 0.0179, seed_999: 0.0178 }
      }
    ],
    decision_tree_comparison: {
      top_feature: "perimeter_worst",
      top_feature_importance: 0.7575,
      explanation: "Trong Decision Tree đơn lẻ, 1 đặc trưng duy nhất chiếm ~75.8% tổng importance do hiệu ứng lấn át ở nút gốc."
    },
    collinearity_analysis: {
      group_size_dimensions: ["perimeter_worst", "radius_worst", "area_worst"],
      group_cell_concavity: ["concave points_mean", "concave points_worst"],
      finding: "Random Forest phân bổ đều trọng số giữa các đặc trưng có tương quan cao (r > 0.95) nhờ kỹ thuật ngẫu nhiên hóa max_features."
    }
  },
  model_metadata: {
    model_name: "WDBC_RandomForest_Classifier_Pipeline",
    version: "1.0.0",
    framework: "scikit-learn 1.9.1",
    created_date: "2026-10-09",
    author: "Đỗ Hữu Quốc Anh",
    institution: "Đại Học Công Nghệ Kỹ Thuật Hưng Yên",
    project: "Project 16 - WDBC Classification",
    pipeline_file: "wdbc_pipeline.joblib",
    sha256_checksum: "1f5c3bc820674e6911d07fd1a372d592bc696e280470903a51276dc4a83451d1",
    input_features_count: 30,
    locked_hyperparameters: {
      n_estimators: 100,
      max_depth: 8,
      min_samples_leaf: 1,
      max_features: 0.3,
      criterion: "gini",
      random_state: 42
    },
    decision_threshold: 0.5,
    training_data_summary: {
      train_samples: 398,
      val_samples: 85,
      total_fit_samples: 483,
      test_samples: 86
    },
    test_performance_metrics: {
      accuracy: 0.9884,
      precision_malignant: 1.0,
      recall_malignant: 0.9688,
      f1_malignant: 0.9841,
      roc_auc: 0.9954,
      confusion_matrix: { tn: 54, fp: 0, fn: 1, tp: 31 }
    },
    clinical_disclaimer: "TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM Y KHOA: Mô hình này được phát triển phục vụ mục đích nghiên cứu học thuật và giáo dục trong học phần Học máy cơ bản tại Đại Học Công Nghệ Kỹ Thuật Hưng Yên. Mô hình TUYỆT ĐỐI KHÔNG ĐƯỢC SỬ DỤNG cho mục đích chẩn đoán y tế hoặc thay thế ý kiến chuyên môn của bác sĩ giải phẫu bệnh."
  }
};
