import sys
import pymysql
import json

BG_COLORS = {
    '20 Minuten': 'rgba(255, 99, 132, 0.2)',
    'Blick': 'rgba(255, 159, 64, 0.2)',
    'Tagesanzeiger': 'rgba(54, 162, 235, 0.2)',
}

COLORS = {
    '20 Minuten': 'rgb(255, 99, 132)',
    'Blick': 'rgb(255, 159, 64)',
    'Tagesanzeiger': 'rgb(54, 162, 235)'
}


def visualize():
    data = {
        'chart1': {
            'labels': [],
            'datasets': [],
        },
        'chart2': {
            'labels': [],
            'datasets': [],
        },
        'chart3': {
            'labels': [],
            'datasets': [{
                'label': 'Anzahl Artikel',
                'data': []
            }],
        }
    }

    connection = pymysql.connect(host='localhost',
                                 user='report',
                                 password=None,
                                 database='news_analyzer',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as c:
        # Gesamtuebersicht
        c.execute('SELECT * FROM PUB_STATISTIC')
        rows = c.fetchall()
        dates = []
        published_per_site = {}
        for row in rows[-120:]:
            dates.append(str(row['PUB_DATE']))
            if row['SITE_NAME'] not in published_per_site:
                published_per_site[row['SITE_NAME']] = []

            published_per_site[row['SITE_NAME']].append(row['PUBLISHED'])

        data['chart1']['labels'] = sorted(list(set(dates)))

        for k in published_per_site.keys():
            data['chart1']['datasets'].append({
                'label': k,
                'data': published_per_site[k],
                'borderColor': COLORS[k],
            })

        # Wochenuebersicht
        c.execute('SELECT * FROM WEEKDAY_STATISTIC')
        rows = c.fetchall()
        published_per_site = {}
        for row in rows:
            if row['SITE_NAME'] not in published_per_site:
                published_per_site[row['SITE_NAME']] = []

            published_per_site[row['SITE_NAME']].append(row['PUBLISHED'])

        data['chart2']['labels'] = ['Montag', 'Dienstag', 'Mittwoch',
                                    'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        for k in published_per_site.keys():
            data['chart2']['datasets'].append({
                'label': k,
                'data': published_per_site[k],
                'borderColor': COLORS[k],
                'backgroundColor': [BG_COLORS[k]],
                'borderWidth': 1
            })

        # Artikel pro Kategorie
        c.execute('SELECT * FROM CATEGORY_SUMMARY')
        rows = c.fetchall()
        for row in rows[-15:]:
            data['chart3']['labels'].append(row['C_NAME'])
            data['chart3']['datasets'][0]['data'].append(row['CNT'])
            data['chart3']['datasets'][0]['backgroundColor'] = 'rgba(255, 159, 64, 0.2)'
            data['chart3']['datasets'][0]['borderColor'] = 'rgb(255, 159, 64)'
            data['chart3']['datasets'][0]['borderWidth'] = '1'

    with open('template.html', 'r') as template:
        content = template.read()
        content = content.replace('##data1##', json.dumps(data['chart1']))
        content = content.replace('##data2##', json.dumps(data['chart2']))
        content = content.replace('##data3##', json.dumps(data['chart3']))

        with open('statistics.html', 'w') as f:
            f.write(content)


if __name__ == '__main__':
    visualize()
