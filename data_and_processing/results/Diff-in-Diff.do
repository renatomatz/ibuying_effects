* Importing the File

clear
import delimited "\\Client\C$\Users\Admin\Downloads\merged_std.csv"

* Processing the Variable 

generate time = (year == 2019) 
generate log_price = log(median_listing_price)

* Processing the Difference-in-Difference Method
ssc install diff
ssc install estout

	* Diff-in-Diff Method without Covariates

eststo: diff log_price, t(treatment) p(time) 
esttab using iBuyer1.tex, se(2)

eststo: diff median_days_on_market, t(treatment) p(time)
esttab using iBuyer2.tex, se(2)


	* Diff-in-Diff Method with Covariates (including number of iBuyers) 

eststo: diff log_price, t(treatment) p(time) cov(median_rooms homeowner_vacancy_rate ///
mean_travel_time_to_work_minutes math_prof_pct english_prof_pct ///
 median_square_feet median_age_years move_post2010 annual_avg_emplvl  ///
 median_household_income_dollars per_capita_income_dollars popestimate ///
 rnaturalinc rnetmig educ_nohs educ_further average_household_size_of_owner_ white ///
 mean_cash_public_assistance_inco construction mean_retirement_income_dollars ntop_ibs nlocal_ibs)report
 esttab using iBuyer3.tex, se(2)

 eststo: diff median_days_on_market, t(treatment) p(time) cov(median_rooms homeowner_vacancy_rate ///
mean_travel_time_to_work_minutes math_prof_pct english_prof_pct ///
 median_square_feet median_age_years move_post2010 annual_avg_emplvl  ///
 median_household_income_dollars per_capita_income_dollars popestimate ///
 rnaturalinc rnetmig educ_nohs educ_further average_household_size_of_owner_ white ///
 mean_cash_public_assistance_inco construction mean_retirement_income_dollars ntop_ibs nlocal_ibs)report
 esttab using iBuyer4.tex, se(2)

	* Diff-in-Diff Method with Covariates (excluding number of iBuyers) 
 
 eststo: diff log_price, t(treatment) p(time) cov(median_rooms homeowner_vacancy_rate ///
mean_travel_time_to_work_minutes math_prof_pct english_prof_pct ///
 median_square_feet median_age_years move_post2010 annual_avg_emplvl  ///
 median_household_income_dollars per_capita_income_dollars popestimate ///
 rnaturalinc rnetmig educ_nohs educ_further average_household_size_of_owner_ white ///
 mean_cash_public_assistance_inco construction mean_retirement_income_dollars)report
 esttab using iBuyer5.tex, se(2)

eststo: diff median_days_on_market, t(treatment) p(time) cov(median_rooms homeowner_vacancy_rate ///
mean_travel_time_to_work_minutes math_prof_pct english_prof_pct ///
 median_square_feet median_age_years move_post2010 annual_avg_emplvl  ///
 median_household_income_dollars per_capita_income_dollars popestimate ///
 rnaturalinc rnetmig educ_nohs educ_further average_household_size_of_owner_ white ///
 mean_cash_public_assistance_inco construction mean_retirement_income_dollars)report
 esttab using iBuyer6.tex, se(2)
