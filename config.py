# config.py

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
]

HEADERS = {
    'User-Agent': USER_AGENTS[0],
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8,es;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'DNT': '1'
}

SELETORES_SITES = {
    'AMAZON': [
        '.a-price-whole',
        '.a-price .a-offscreen',
        '.a-price-range .a-price .a-offscreen',
        '.apexPriceToPay .a-offscreen',
        '#priceblock_dealprice',
        '#priceblock_ourprice',
        '#corePrice_desktop .a-price .a-offscreen',
        '.a-price[data-a-size="xl"]'
    ],
    'MERCADO_LIVRE': [
        '.andes-money-amount__fraction',
        '.ui-prixe-price__part',
        '.ui-pdp-price__second-line',
        '.ui-pdp-price__size--large',
        '.ui-pdp-price__part'
    ],
    'MAGAZINE_LUIZA': [
        '[data-testid="price-value"]',
        '.price-template__text',
        '.final-price',
        '.price-box__row'
    ],
    'AMERICANAS': [
        '.src__BestPrice-sc-1jvw02c-5',
        '.price__SalesPrice-ej7lo8-2',
        '.main-price'
    ],
    'SUBMARINO': [
        '.src__BestPrice-sc-1jvw02c-5',
        '.price__SalesPrice-ej7lo8-2'
    ],
    'WEBMOTORS': [
        '.Price__PriceValue-sc-10n3h66',
        '.jss180',
        '[data-testid="price"]'
    ],
    'OLX': [
        '.ad__sc-1le2d5e-0',
        '.sc-ifAKCX',
        '.sc-bwCtUz'
    ],
    'DELL': [
        '.ps-dell-price',
        '.final-price',
        '.price',
        '[data-testid="sharedPSPrice"]'
    ]
}

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'seuemail@gmail.com',
    'senha': 'sua_senha_app'
}