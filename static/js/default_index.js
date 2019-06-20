// This is the js for the default/index.html view.

var app = function() {

    var self = {};

    Vue.config.silent = false; // show all warnings

    // Extends an array
    self.extend = function(a, b) {
        for (var i = 0; i < b.length; i++) {
            a.push(b[i]);
        }
    }; 
    var enumerate = function(v) { var k=0; return v.map(function(e) {e._idx = k++;});};

    self.do_search = function () {
        self.hide();
        $.getJSON(search_url,
            {search_string: self.vue.search_string},
            function (data) {
                self.vue.product_list = data.product_list;
            });
        self.process_search();
    };

    self.getcart =function(){
        $.getJSON(get_cart_url,
            {},
            function (data){
                self.vue.cart = data.cart;
            });
    }

    self.process_search = function() {
        self.vue.product_list.map (function(e){
            Vue.set(e, '_num_stars_display', e.average);
        });
    };

    self.initializereview = function(_id){
        $.getJSON(initializereview_url,
            {product: _id});
    };

    self.hide = function() {
        self.vue.product_list.map(function (e){
            Vue.set(e, "_details", false);
        });
        self.vue.review_list = [];
    };

    self.show = function(_id) {
        $.getJSON(get_reviews, {product: _id},
            function (data) {
                self.vue.review_list = data.review_list;
            });
        self.initializereview(_id);
        $.getJSON(get_own_review, {product: _id},
            function (data) {
                self.vue.selfreview = data.review;
                self.vue.product_list.map(function (e){
                    if (e.id == _id){
                        Vue.set(e, "_details", true);
                    } else {
                        Vue.set(e, "_details", false);
                    }
                });
        });
    };

    self.stars_out = function (p) {
        $.getJSON(get_own_review, {product: p.id},
            function (data) {
                self.vue.selfreview = data.review;
            });
        self.vue.selfreview.map(function (e){
            Vue.set(e, '_num_stars_display', e.stars)
        });
    };

    self.stars_over = function(star_idx) {
        self.vue.selfreview.map(function (e){
            Vue.set(e, '_num_stars_display', star_idx)
        });
    }; 

    self.set_stars = function(p, star_idx){
        $.getJSON(set_stars_url, {
            product_id: p.id,
            rating: star_idx
        });
        $.getJSON(get_own_review, {product: p.id},
            function (data) {
                self.vue.selfreview = data.review;
            });
        self.vue.selfreview.map(function (e){
            Vue.set(e, '_num_stars_display', star_idx)
        });
    };

    self.add_review = function (p, r) {
        // We disable the button, to prevent double submission.
        $.web2py.disableElement($("#review-button"));
        var sent_content = self.vue.form_content; // 
        $.getJSON(add_review_url,
            // Data we are sending.
            {
                product_id:p.id,
                post_content: r.review
            },
            // What do we do when the post succeeds?
            function (data) {
                // Re-enable the button.
                $.web2py.enableElement($("#review-button"));
                self.vue.check = true;
                setTimeout(function() {
                    self.vue.check = false;},10000);
            });
        // If you put code here, it is run BEFORE the call comes back.
    };
    self.inc_desired_quantity = function (pid, n){
        self.vue.product_list.map(function (e){
            if (e.id == pid){
                Vue.set(e, "desired_quantity", e.desired_quantity + n);
            }
        });
    }

    self.buy_product = function(pid){
        $.web2py.disableElement($("#buy_buttons"));
        self.vue.product_list.map(function (e){
            if (e.id == pid){
                $.getJSON(buy_product_url,
                {
                    product_id:pid,
                    quantity:e.desired_quantity
                },
                function (data){
                    $.web2py.enableElement($("#buy_buttons"));
                });
            }
        });
    }

    self.goto = function(mode){
        self.vue.page = mode;
        self.getcart();
        self.processcart();
    }
    
    self.processcart = function(){
        self.vue.total = 0;
        self.vue.cart.map (function(e){
            self.vue.total += e.cost;
        });
    }

    self.clearcart = function(){
        $.getJSON(clear_cart_url,
            {}
        );
        self.vue.cart = [];
    }
    // self.add_review = function () {
    //     // We disable the button, to prevent double submission.
    //     $.web2py.disableElement($("#add-product"));
    //     var sent_title = self.vue.form_title; // Makes a copy 
    //     var sent_content = self.vue.form_content; // 
    //     $.post(add_product_url,
    //         // Data we are sending.
    //         {
    //             product_title: self.vue.form_title,
    //             post_content: self.vue.form_content
    //         },
    //         // What do we do when the post succeeds?
    //         function (data) {
    //             // Re-enable the button.
    //             $.web2py.enableElement($("#add-post"));
    //             // Clears the form.
    //             self.vue.form_title = ""; 
    //             self.vue.form_content = "";
    //             // Adds the post to the list of posts. 
    //             var new_post = {
    //                 id: data.post_id,
    //                 post_title: sent_title,
    //                 post_content: sent_content
    //             };
    //             self.vue.post_list.unshift(new_post);
    //             // We re-enumerate the array.
    //             self.process_posts();
    //         });
    //     // If you put code here, it is run BEFORE the call comes back.
    // };
    // Complete as needed.
    self.vue = new Vue({
        el: "#vue-div",
        delimiters: ['${', '}'],
        unsafeDelimiters: ['!{', '}'],
        data: {
            form_title: "",
            form_content: '',
            product_list: [],
            cart: [],
            total: 0,
            search_string: '',
            _details: 0,
            review_list: [],
            selfreview: [],
            star_indices: [1, 2, 3, 4, 5],
            check: false,
            page: 'shop'
        },
        methods: {
            do_search: self.do_search,
            show: self.show,
            hide: self.hide,
            stars_out: self.stars_out,
            stars_over: self.stars_over,
            set_stars: self.set_stars,
            add_review: self.add_review,
            inc_desired_quantity: self.inc_desired_quantity,
            getcart: self.getcart,
            buy_product: self.buy_product,
            processcart: self.processcart,
            clearcart: self.clearcart,
            goto: self.goto
        }

    });

    self.do_search();
    return self;
};

var APP = null;

// This will make everything accessible from the js console;
// for instance, self.x above would be accessible as APP.x
jQuery(function(){APP = app();});
