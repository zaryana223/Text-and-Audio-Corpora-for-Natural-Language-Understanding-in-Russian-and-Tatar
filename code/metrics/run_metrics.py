import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from nlu_metrics.csv_builder import create_comparison_csv
from nlu_metrics.metrics import per_slot_f1, save_per_slot, score


def main():
    parser = argparse.ArgumentParser(
        description="NLU metrics: intent accuracy/F1, span F1, joint; ASR-aware slot F1 for GigaAM."
    )
    parser.add_argument("--gold", required=True, help="Gold CoNLL file (.conll)")
    parser.add_argument("--pred", required=True, help="Prediction CoNLL/out file")
    parser.add_argument("--model", required=True, help="Model name (use gigaam in name for ASR metrics)")
    parser.add_argument(
        "--output-dir",
        default="results",
        help="Directory for comparison CSV and metrics summary",
    )
    parser.add_argument(
        "--no-per-slot",
        action="store_true",
        help="Skip per-slot breakdown CSV",
    )
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    model_name = args.model
    comparison_csv = out_dir / f"comparison_{model_name}.csv"
    summary_csv = out_dir / "metrics_summary.csv"
    df = create_comparison_csv(
        args.gold,
        args.pred,
        str(comparison_csv),
        pred_name=model_name,
    )
    print(f"Saved comparison: {comparison_csv}")
    score(df, model_name=model_name, save_path=str(summary_csv))
    if not args.no_per_slot:
        per_slot_df = per_slot_f1(df, model_name)
        save_per_slot(per_slot_df, model_name, output_dir=str(out_dir))


if __name__ == "__main__":
    main()
