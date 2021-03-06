def find_tag(dom, tag_name):
    tags = dom.getElementsByTagName(tag_name)
    if tags:
        return tags
    breakable_tag = tag_name.split(':')
    broken_tags = breakable_tag[-1].split('.')
    if len(broken_tags) < 2:
        return tags
    tag_till_now = breakable_tag[0] + ':' if len(breakable_tag) > 1 else ''
    for i, tag in enumerate(broken_tags):
        tag_till_now += tag
        sub_tags = dom.getElementsByTagName(tag_till_now)
        if sub_tags:
            for sub_tag in sub_tags:
                try:
                    remaining_tag = '.'.join(broken_tags[i+1:])
                    found_sub_tags = find_tag(sub_tag, remaining_tag)
                    if found_sub_tags:
                        return found_sub_tags
                except IndexError:
                    pass
        tag_till_now += '.'


def get_parent_with_tag_or_variable(dom, node, tag):
    while node:
        if node.tagName == tag:
            return node
        if node.tagName == 'match:variable':
            var_name = node.getAttribute('name')
            variables = utils.find_tag(dom, 'name')
            for variable in variables:
                if variable.firstChild.data == var_name:
                    tags = get_parent_with_tag_or_variable(dom, variable, tag)
                    if tags:
                        return tags
        node = node.parentNode
