//选中菜单
$(".menu-nor").click(function () {
    $(this).addClass("menu-active");
    $(".menu-nor").not(this).removeClass("menu-active");
});