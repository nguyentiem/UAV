"""Smoke check the generated course in a real local-file Chrome session."""
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

root = Path(__file__).parent
opts = Options()
opts.add_argument('--headless=new')
opts.add_argument('--disable-gpu')
opts.add_argument('--no-sandbox')
opts.add_argument('--window-size=1400,900')
opts.set_capability('goog:loggingPrefs', {'browser':'ALL'})
driver = webdriver.Chrome(options=opts)
try:
    driver.get((root / 'nen-tang-toan.html').as_uri())
    foundation = driver.execute_script("""
      return {sources:document.querySelectorAll('[data-math]').length,
        rendered:document.querySelectorAll('[data-math] .katex').length,
        errors:[...document.querySelectorAll('[data-math]')].filter(e=>e.title).map(e=>e.title),
        canvas:[...document.querySelectorAll('canvas')].map(e=>e.width)};
    """)
    if foundation['errors']:
        print(driver.execute_script("return [...document.querySelectorAll('[data-math]')].filter(e=>e.title).map(e=>e.dataset.math)"))
    assert foundation['sources'] == foundation['rendered'] and not foundation['errors'], foundation
    assert all(width > 0 for width in foundation['canvas']), foundation
    assert not [item for item in driver.get_log('browser') if item['level'] == 'SEVERE']
    print('00: OK')
    for n in range(1, 18):
        driver.get((root / f'bai-{n:02}.html').as_uri())
        driver.implicitly_wait(2)
        state = driver.execute_script("""
          const e=document.querySelector('[data-math]');
          return {title:document.title,math:!!e.querySelector('.katex'),
            errors:document.querySelectorAll('.katex-error').length,
            sources:document.querySelectorAll('[data-math]').length,
            rendered:document.querySelectorAll('[data-math] .katex').length,
            canvas:document.querySelector('canvas').width,
            output:document.querySelector('#readout').textContent,
            links:[...document.querySelectorAll('nav a')].map(a=>a.getAttribute('href'))};
        """)
        assert state['math'] and state['errors'] == 0 and state['sources'] == state['rendered'], (n,state)
        assert state['canvas'] > 0 and state['output'], (n,state)
        assert all((root / link).exists() for link in state['links']), (n,state)
        if n in (1,2):
            rotor = driver.execute_script("return document.querySelector('#rotor-output').textContent")
            assert 'τx=0.000' in rotor and 'τy=0.000' in rotor and 'τz=0.000' in rotor, rotor
            driver.execute_script("const r=document.querySelector('.rotor-input');r.value=Number(r.value)+1;r.dispatchEvent(new Event('input',{bubbles:true}))")
            changed = driver.execute_script("return document.querySelector('#rotor-output').textContent")
            assert changed != rotor, (n,rotor,changed)
        driver.execute_script("const r=document.querySelector('#param'); r.value=r.max; r.dispatchEvent(new Event('input',{bubbles:true}));")
        driver.execute_script("document.querySelector('#pause').click()")
        assert driver.find_element(By.ID, 'pause').text == 'Tiếp tục'
        driver.execute_script("document.querySelector('#reset').click()")
        assert driver.find_element(By.ID, 'pause').text == 'Tạm dừng'
        assert driver.execute_script("return document.querySelector('#param').value == JSON.parse(document.querySelector('#lesson-config').textContent).initial")
        assert not [item for item in driver.get_log('browser') if item['level'] == 'SEVERE'], n
        print(f'{n:02}: OK')
    driver.set_window_size(390,844)
    for name in ['nen-tang-toan.html','bai-01.html','bai-02.html','bai-03.html','bai-17.html']:
        driver.get((root / name).as_uri())
        assert driver.execute_script('return document.documentElement.scrollWidth <= innerWidth + 2'), name
    print('Mobile width: OK')
finally:
    driver.quit()
