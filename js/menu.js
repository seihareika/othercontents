$(".openbtn4").click(function () {
    $(this).toggleClass('active');
    $("#g-nav").toggleClass('panelactive');
});

$("#g-nav a").click(function () {//ナビゲーションのリンクがクリックされたら
    $(".openbtn4").removeClass('active');//ボタンの activeクラスを除去し
    $("#g-nav").removeClass('panelactive');//ナビゲーションのpanelactiveクラスも除去
});