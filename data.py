class Case:
    def __init__(self, case_number, case_name, year, offence, outcome):
        self.case_number = case_number
        self.case_name = case_name.lower()
        self.year = year
        self.offence = offence
        self.outcome = outcome.strip('\n')
        if "appeal" in self.case_name.lower():
            self.type = "appeal"
        else:
            self.type = "charge"

    def __str__(self):
        attributes = vars(self)
        return ', '.join("%s: %s" % item for item in attributes.items())


def get_cases(path):
    res = []
    with open(path, 'r') as file:
        for line in file:
            line = line.split(',')
            case = Case(case_number=line[0],
                        case_name=line[1],
                        year=line[2],
                        offence=line[3],
                        outcome=line[4])
            res.append(case)
    del res[0]
    return res


def create_flow(cases):
    res = {'charge': {}, 'appeal': {}}
    for case in cases:
        tup = (case.offence, case.outcome)

        if tup not in res[case.type]:
            res[case.type][tup] = 1
        else:
            res[case.type][tup] += 1
    return res


def get_types(cases):
    res = {}
    charges = 0
    appeals = 0
    for case in cases:
        if case.type == "appeal":
            appeals += 1
        else:
            charges += 1
    res['charges'] = charges
    res['appeals'] = appeals
    res['total'] = charges + appeals
    return res


def merge_dicts(d1, d2):
    new = {}
    for k, v in d1.items():
        new[k] = v
    for k, v in d2.items():
        if k not in new:
            new[k] = v
        else:
            new[k] += v
    return new


def create_single(d1):
    new = {}
    for k, v in d1.items():
        if k[0] not in new:
            new[k[0]] = v
        else:
            new[k[0]] += v
    return new


def run(cases):
    d = create_flow(cases)

    label = ['Cases', 'Charges', 'Appeals']
    source = []
    target = []
    values = []
    merged = merge_dicts(d['charge'], d['appeal'])

    labels = {'Impersonation': 3,
              'Unauthorized aid': 4,
              'Plagiarism and/or purchased essay': 5,
              'Creating false data and/or fabricating academic sources': 6,
              'Forgery of Documents': 7,
              'Academic Dishonesty Not Otherwise Described': 8,
              'Forgery of Academic Records': 9,
              'Providing Unauthorized Assistance': 10,
              'Grade Assignment of 0 for course': 11,
              'Notation on transcript': 12,
              'Suspension': 13,
              'Expulsion': 14,
              'Acquittal': 15,
              'Degree suspension or recall': 16,
              'Denial of Privileges': 17,
              'Reduced Grade': 18,
              }

    colors_map = {'Impersonation': "rgba(102, 102, 255, 0.8)",
                  'Unauthorized aid': "rgba(255, 127, 14, 0.8)",
                  'Plagiarism and/or purchased essay': "rgba(44, 160, 44, 0.8)",
                  'Creating false data and/or fabricating academic sources': "rgba(214, 39, 40, 0.8)",
                  'Forgery of Documents': "rgba(140, 86, 75, 0.8)",
                  'Academic Dishonesty Not Otherwise Described': "rgba(227, 119, 194, 0.8)",
                  'Forgery of Academic Records': "rgba(23, 190, 207, 0.8)",
                  'Providing Unauthorized Assistance': "rgba(31, 119, 180, 0.8)"}

    colors = []

    for key, value in labels.items():
        label.append(key)

    for key, value in create_single(d['charge']).items():
        source.append(1)
        target.append(labels[key])
        values.append(value)
        colors.append("rgba(141, 141, 126, 0.8)")

    for key, value in create_single(d['appeal']).items():
        source.append(2)
        target.append(labels[key])
        values.append(value)
        colors.append("grey")

    for key, value in merged.items():
        source.append(labels[key[0]])
        target.append(labels[key[1]])
        values.append(value)
        colors.append(colors_map[key[0]])

    _data = dict(
        type='sankey',
        node=dict(
            pad=15,
            thickness=40,
            line=dict(
                color="black",
                width=0.5
            ),
            label=label,
            color=["black", "rgba(141, 141, 126, 0.8)", "grey",
                   "rgba(102, 102, 255, 0.8)",
                   "rgba(255, 127, 14, 0.8)",
                   "rgba(44, 160, 44, 0.8)",
                   "rgba(214, 39, 40, 0.8)",
                   "rgba(140, 86, 75, 0.8)",
                   "rgba(227, 119, 194, 0.8)",
                   "rgba(23, 190, 207, 0.8)",
                   "rgba(31, 119, 180, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)",
                   "rgba(236, 232, 217, 0.8)"]
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color=colors,
            line=dict(
                width=[100, 1, 200]
            )
        )
    )

    return _data


_cases = get_cases('output.csv')
data = run(_cases)
