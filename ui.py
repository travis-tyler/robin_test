import click

def success(message):
    click.echo(click.style(str(message), fg='green', bold=True))

def error(message):
    click.echo(click.style(str(message), fg='red', bold=True))

def bar():
    click.echo(click.style('=============', fg='green', bold=True))

def chec_ref(result):
    if 'ref_id' in result:
        success(result)
    else:
        error(result)