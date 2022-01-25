window.onload = function () {
    let quantity, _price, orderitem_num, delta_quantity, orderitem_quantity,delta_cost;
    const quantity_arr = [];
    const price_arr = [];
    const TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());
    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_cost = parseFloat($('.order_total_cost').text().replace(',', '.')) || 0;

    for (let i=0; i < TOTAL_FORMS; i++) {
        quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.')) ;
        quantity_arr[i] = quantity;
        if (price) {
            price_arr[i] = price;
        } else {
            price_arr[i] = 0;
        }
    }
    console.info('QUANTITY', quantity_arr)
    console.info('PRICE', price_arr)


    if (!order_total_quantity) {
        for (var i=0; i < TOTAL_FORMS; i++) {
            order_total_quantity += quantity_arr[i];
            order_total_cost += quantity_arr[i] * price_arr[i];
            }
            console.log(order_total_quantity)
            console.log(order_total_cost)
            $('.order_total_quantity').html(order_total_quantity.toString());
            $('.order_total_cost').html(Number(order_total_cost.toFixed(2)).toString());
    };

    $('.order_form').on('click', 'input[type="number"]', function () {
        var target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        //уголок любопытного питониста
        console.log('target: ' + target);
        console.log('orderitem_num: ' + orderitem_num);

        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
            //уголок любопытного питониста
            console.log('price_arr[orderitem_num]: ' + price_arr[orderitem_num])
            console.log('orderitem_quantity: ' + orderitem_quantity)
            console.log('delta_quantity: ' + delta_quantity)
            console.log('quantity_arr[orderitem_num]: ' + quantity_arr[orderitem_num])
            }
        });

    $('.formset_row').formset({
            addText: 'добавить продукт',
            deleteText: 'удалить',
            prefix: 'orderitems',
            removed: deleteOrderItem
            });

    $(document).on('change', '.form-control', function() {
            let target = event.target;
            orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
            let orderitem_product_pk = target.options[target.selectedIndex].value;
//            console.log(orderitem_num);
//            console.log(orderitem_product_pk);
            if (orderitem_product_pk){
                $.ajax({
                url:'/orders/product/' + orderitem_product_pk + '/price/',
                success: function(data) {
                    if(data.price){
                        price_arr[orderitem_num] = parseFloat(data.price)
                        if (isNaN(quantity_arr[orderitem_num])){
                            quantity_arr[orderitem_num] = 0;
                            }
                        let price_html = '<span class="orderitems-' + orderitem_num + 'price">'
                            + data.price.toString().replace('.', ',') + '</span> руб';
                        let current_tr = $('.order_form table').find('tr:eq('+(orderitem_num+1)+')');
                        current_tr.find('td:eq(2)').html(price_html);
                        }
                    }
                })
            }



            });


//    $('.order_form').on('click', 'input[type="checkbox"]', function () {
//        var target = event.target;
//        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
//        if (target.checked) {
//            delta_quantity = -quantity_arr[orderitem_num];
//        } else {
//            delta_quantity = quantity_arr[orderitem_num];
//        }
//        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
//        });

    function deleteOrderItem(row) {
        var target_name= row[0].querySelector('input[type="number"]').name;
        console.log('target_name: ' + target_name)
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));
        console.log('orderitem_num: ' + orderitem_num)
        delta_quantity = -quantity_arr[orderitem_num];
        console.log('delta_quantity: ' + delta_quantity)
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    };

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        console.log('orderitem_price: ' + orderitem_price)
        console.log('delta_quantity: ' + delta_quantity)
        delta_cost = orderitem_price * delta_quantity;
        console.log('delta_cost: ' + delta_cost)
        order_total_cost = Number((order_total_cost + delta_cost).toFixed(2));
        console.log('order_total_cost: ' + order_total_cost)
        order_total_quantity = order_total_quantity + delta_quantity;
        console.log('order_total_quantity: ' + order_total_quantity)
        $('.order_total_cost').html(order_total_cost.toString());
        $('.order_total_quantity').html(order_total_quantity.toString());
        };


}