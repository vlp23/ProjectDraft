import ParameterClasses as P
import MarkovModel as MarkovCls
import SupportMarkovModel as SupportMarkov

# NO TREATMENT
# create a cohort
cohort_none = MarkovCls.Cohort(id=0, therapy=P.Therapies.NONE)
simOutputs_none = cohort_none.simulate()

# ANTICOAG
# create a cohort
cohort_anticoag = MarkovCls.Cohort(id=1, therapy=P.Therapies.ANTICOAG)
simOutputs_anticoag = cohort_anticoag.simulate()

# draw survival curves and histograms
SupportMarkov.draw_survival_curves_and_histograms(simOutputs_none, simOutputs_anticoag)

# print the estimates
SupportMarkov.print_outcomes(simOutputs_none, "No therapy")
SupportMarkov.print_outcomes(simOutputs_anticoag, "Anticoagulation theraoy")

# print comparative outcomes
SupportMarkov.print_comparative_outcomes(simOutputs_none, simOutputs_anticoag)

# report the CEA results
SupportMarkov.report_CEA_CBA(simOutputs_none, simOutputs_anticoag)

