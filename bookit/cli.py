import click

from .api_client import ApiClient


@click.group()
@click.option('--username')
@click.option('--password')
@click.pass_context
def cli(ctx, username, password):
	ctx.obj = ApiClient(username, password)


@cli.group()
def resource():
	pass


@cli.group()
def booking():
	pass


@booking.command()
@click.argument('start_time')
@click.argument('end_time')
@click.argument('booking_date')
@click.argument('resource_id')
@click.option('--email-receipt', required=True, default=False)
@click.pass_obj
def create(client, start_time, end_time, booking_date, resource_id, email_receipt):
	print(client.create_booking(start_time, end_time, booking_date, resource_id, email_receipt))


@booking.command()
@click.argument('booking_id')
@click.option('--email-receipt', required=True, default=False)
@click.pass_obj
def delete(client, booking_id, email_receipt):
	print(client.delete_booking(booking_id, email_receipt))


@booking.command()
@click.pass_obj
def list(client):
	print(client.list_bookings())


if __name__ == '__main__':
	try:
		cli(auto_envvar_prefix='BOOKIT')
	except Exception as e:
		print(e)

