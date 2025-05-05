
import { patch } from "@web/core/utils/patch";
import { AccountReportFilters } from "@account_reports/components/account_report/filters/filters";

patch(AccountReportFilters.prototype, {
    async filterAccountClick({ optionKey, optionValue = undefined, reload = false})
            {
                if(optionKey !== undefined)
                {
                   optionKey.selected = !optionKey.selected;
                   let selected = this.controller.options.account_id.filter((item)=> {return item.selected == true;})
                   await this.controller.updateOption('account_id', this.controller.options.account_id,true);
                }
            }
    });


