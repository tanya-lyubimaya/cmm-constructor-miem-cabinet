<template>
  <div class="wrapper">
        <div class="navigation">
            <section class="container">
                <a class="navigation-title" href="/enter" title="База КИМов - Сервис для преподавателей МИЭМ НИУ ВШЭ">
                    <h1 class="title">База КИМов</h1>
                </a>
            </section>
        </div>
        <section class="container" id="base">
            <h3 class="title">База КИМов</h3>
            <div id="enterNameOfCMM" style="display: none">
            </div>
            <br>
            <br><br><br>
            <h3 class="title">Мои курсы</h3>
        </section>
  </div>
</template>

<style>
    .wrapper {
    display: block;
    overflow: hidden;
    overflow-x: hidden;
    overflow-y: hidden;
    position: relative;
    width: 100%;
}
    .navigation {
        background: #f4f5f6;
        border-bottom: .1rem solid #d1d1d1;
        display: block;
        height: 5.2rem;
        left: 0;
        max-width: 100%;
        position: fixed;
        right: 0;
        top: 0;
        width: 100%;
        z-index: 1;
    }
    .navigation .navigation-link, .navigation .navigation-title, .navigation .title {
        display: inline;
        font-size: 1.6rem;
        line-height: 5.2rem;
        padding: 0;
        text-decoration: none;
        margin: 30px;
    }
    .navigation .navigation-title, .navigation .title {
        color: #606c76;
        font-family: Roboto,sans-serif;
        position: relative;
        font-size: 2rem;
    }
    a {
        color: #9b4dca;
        text-decoration: none;
    }
    p {
        margin-top: 0;
    }
        .header .button {
        margin-bottom: 4rem;
        margin-top: 2rem;
    }
    .header .img path {
        animation: 7s a forwards;
        fill: #9b4dca;
        stroke: #9b4dca;
        stroke-dasharray: 38321;
        stroke-miterlimit: 10;
        stroke-width: 2px;
    }
    .wrapper>.container {
        padding-bottom: 7.5rem;
        padding-top: 7.5rem;
    }
    #base {
        max-width: 100rem;
    }
    .container {
        margin: 0 auto;
        padding: 0 2.0rem;
        position: relative;
        width: 100%;
    }
    h3 {
        font-size: 2.8rem;
        line-height: 1.3;
    }
    .button-clear {
        font-size: 0.9rem;
        height: 2.8rem;
        line-height: 2.8rem;
        padding: 0 2.3rem;
    }
    .footer {
        padding: 8rem 0 2rem;
    }
    .footer .copyright {
        padding-right: 7rem;
        padding-left: 7rem;
    }
    .footer .nav {
        position: absolute;
        right: 2rem;
        top: 50%;
        transform: translateY(-50%);
    }
    .footer .nav .link {
        display: inline-block;
        margin-left: 1.2rem;
        padding: 0;
    }
    .footer .nav .icon {
        fill: #9b4dca;
        height: 2rem;
    }
</style>