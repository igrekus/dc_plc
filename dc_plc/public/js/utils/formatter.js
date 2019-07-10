let product_link_formatter = (value, row, column, row_data, format) => {
    if (!value) {
        value = '-';
    }

    if (column.id === __('Relevance')) {
        let id = row[1].content;
        let [date, check, perms] = value.split(';');
        let check_str = parseInt(check) ? 'checked' : '';
        if (parseInt(perms)) {
            return `<input type="checkbox" id="${id}" onchange="check_handle(this)" ${check_str}/><label style="vertical-align: top; padding-top: 3px;" class="rel_label_${id}" for="${id}">&nbsp&nbsp${date}</label>`
        }
        value = date;
    }
    return `<a href="http://${window.location.host}/desk#Form/DC_PLC_Product_Summary/${row_data.ID}">${value}</a>`;
};
