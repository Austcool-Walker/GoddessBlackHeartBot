import asyncio, aiohttp, discord
import os, sys, linecache, traceback, glob
import re, json, random, math, html
import wand, wand.color, wand.drawing
import PIL, PIL.Image, PIL.ImageFont, PIL.ImageOps, PIL.ImageDraw
import numpy as np
import cairosvg, urbandict
import pixelsort.sorter, pixelsort.sorting, pixelsort.util, pixelsort.interval
import hashlib, base64
from urllib.parse import parse_qs
from lxml import etree
from imgurpython import ImgurClient
from io import BytesIO, StringIO
from discord.ext import commands
from pyfiglet import figlet_format
from string import ascii_lowercase as alphabet
from urllib.parse import quote
from concurrent.futures._base import CancelledError
from Utils import Checks

code = "```py\n{0}\n```"

#http://stackoverflow.com/a/34084933
#for google_scrap
def get_deep_text(element):
	try:
		text = element.text or ''
		for subelement in element:
		  text += get_deep_text(subelement)
		text += element.tail or ''
		return text
	except:
		return ''

def posnum(num): 
	if num < 0 : 
		return - (num)
	else:
		return num

def find_coeffs(pa, pb):
	matrix = []
	for p1, p2 in zip(pa, pb):
		matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
		matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])
	A = np.matrix(matrix, dtype=np.float)
	B = np.array(pb).reshape(8)
	res = np.dot(np.linalg.inv(A.T*A)*A.T, B)
	return np.array(res).reshape(8)

class Fun2(commands.Cog, name="Fun2"):
	def __init__(self, bot):
		self.bot = bot

		self.is_nsfw = bot.funcs.is_nsfw

	@commands.command(pass_context=True)
	async def badmeme(self, ctx, direct=None):
		"""returns bad meme (shit api)"""
		load = await self.get_json("https://api.imgflip.com/get_memes")
		url = random.choice(load['data']['memes'])
		url = url['url']
		if direct:
			await ctx.send(url)
		else:
			b = await self.bytes_download(url)
			await self.bot.upload(b, filename='badmeme.png')

	def do_magik(self, scale, *imgs):
		try:
			list_imgs = []
			exif = {}
			exif_msg = ''
			count = 0
			for img in imgs:
				i = wand.image.Image(file=img)
				i.format = 'jpg'
				i.alpha_channel = True
				if i.size >= (3000, 3000):
					return ':warning: `Image exceeds maximum resolution >= (3000, 3000).`', None
				exif.update({count:(k[5:], v) for k, v in i.metadata.items() if k.startswith('exif:')})
				count += 1
				i.transform(resize='800x800>')
				i.liquid_rescale(width=int(i.width * 0.5), height=int(i.height * 0.5), delta_x=int(0.5 * scale) if scale else 1, rigidity=0)
				i.liquid_rescale(width=int(i.width * 1.5), height=int(i.height * 1.5), delta_x=scale if scale else 2, rigidity=0)
				magikd = BytesIO()
				i.save(file=magikd)
				magikd.seek(0)
				list_imgs.append(magikd)
			if len(list_imgs) > 1:
				imgs = [PIL.Image.open(i).convert('RGBA') for i in list_imgs]
				min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
				imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
				imgs_comb = PIL.Image.fromarray(imgs_comb)
				ya = BytesIO()
				imgs_comb.save(ya, 'png')
				ya.seek(0)
			elif not len(list_imgs):
				return ':warning: **Command download function failed...**', None
			else:
				ya = list_imgs[0]
			for x in exif:
				if len(exif[x]) >= 2000:
					continue
				exif_msg += '**Exif data for image #{0}**\n'.format(str(x+1))+code.format(exif[x])
			else:
				if len(exif_msg) == 0:
					exif_msg = None
			return ya, exif_msg
		except Exception as e:
			return str(e), None

	@commands.command(pass_context=True, aliases=['imagemagic', 'imagemagick', 'magic', 'magick', 'cas', 'liquid'])
	async def magik(self, ctx, *urls:str):
		"""Apply magik to Image(s)\n .magik image_url or .magik image_url image_url_2"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=6, scale=5)
			if not get_images:
				return
			img_urls = get_images[0]
			scale = get_images[1]
			scale_msg = get_images[2]
			if scale_msg is None:
				scale_msg = ''
			msg = await self.bot.send_message(ctx.message.channel, "ok, processing")
			list_imgs = []
			for url in img_urls:
				b = await self.bytes_download(url)
				if b is False:
					if len(img_urls) > 1:
						await ctx.send(':warning: **Command download function failed...**')
						return
					continue
				list_imgs.append(b)
			final, content_msg = await self.bot.loop.run_in_executor(None, self.do_magik, scale, *list_imgs)
			if type(final) == str:
				await ctx.send(final)
				return
			if content_msg is None:
				content_msg = scale_msg
			else:
				content_msg = scale_msg+content_msg
			await self.bot.delete_message(msg)
			await self.bot.upload(final, filename='magik.png', content=content_msg)
		except discord.errors.Forbidden:
			await ctx.send(":warning: **I do not have permission to send files!**")
		except Exception as e:
			await ctx.send(e)

	def do_gmagik(self, ctx, gif, gif_dir, rand):
		try:
			try:
				frame = PIL.Image.open(gif)
			except:
				return ':warning: Invalid Gif.'
			if frame.size >= (3000, 3000):
				os.remove(gif)
				return ':warning: `GIF resolution exceeds maximum >= (3000, 3000).`'
			nframes = 0
			while frame:
				frame.save('{0}/{1}_{2}.png'.format(gif_dir, nframes, rand), 'GIF')
				nframes += 1
				try:
					frame.seek(nframes)
				except EOFError:
					break
			imgs = glob.glob(gif_dir+"*_{0}.png".format(rand))
			if len(imgs) > 150 and ctx.message.author.id != self.bot.owner.id:
				for image in imgs:
					os.remove(image)
				os.remove(gif)
				return ":warning: `GIF has too many frames (>= 150 Frames).`"
			for image in imgs:
				try:
					im = wand.image.Image(filename=image)
				except:
					continue
				i = im.clone()
				i.transform(resize='800x800>')
				i.liquid_rescale(width=int(i.width*0.5), height=int(i.height*0.5), delta_x=1, rigidity=0)
				i.liquid_rescale(width=int(i.width*1.5), height=int(i.height*1.5), delta_x=2, rigidity=0)
				i.resize(i.width, i.height)
				i.save(filename=image)
			return True
		except Exception as e:
			exc_type, exc_obj, tb = sys.exc_info()
			f = tb.tb_frame
			lineno = tb.tb_lineno
			filename = f.f_code.co_filename
			linecache.checkcache(filename)
			line = linecache.getline(filename, lineno, f.f_globals)
			print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

	@commands.command(pass_context=True)
	async def gmagik(self, ctx, url:str=None, framerate:str=None):
		try:
			url = await self.get_images(ctx, urls=url, gif=True, limit=2)
			if url:
				url = url[0]
			else:
				return
			gif_dir = self.files_path('gif/')
			check = await self.isgif(url)
			if check is False:
				await ctx.send("Invalid or Non-GIF!")
				ctx.command.reset_cooldown(ctx)
				return
			x = await self.bot.send_message(ctx.message.channel, "ok, processing (this might take a while for big gifs)")
			rand = self.bot.random()
			gifin = gif_dir+'1_{0}.gif'.format(rand)
			gifout = gif_dir+'2_{0}.gif'.format(rand)
			await self.download(url, gifin)
			if os.path.getsize(gifin) > 5000000 and ctx.message.author.id != self.bot.owner.id:
				await ctx.send(":no_entry: `GIF Too Large (>= 5 mb).`")
				os.remove(gifin)
				return
			try:
				result = await self.bot.loop.run_in_executor(None, self.do_gmagik, ctx, gifin, gif_dir, rand)
			except CancelledError:
				await ctx.send(':warning: Gmagik failed...')
				return
			if type(result) == str:
				await ctx.send(result)
				return
			if framerate != None:
				args = ['ffmpeg', '-y', '-nostats', '-loglevel', '0', '-i', gif_dir+'%d_{0}.png'.format(rand), '-r', framerate, gifout]
			else:
				args = ['ffmpeg', '-y', '-nostats', '-loglevel', '0', '-i', gif_dir+'%d_{0}.png'.format(rand), gifout]
			await self.bot.run_process(args)
			await self.bot.upload(gifout, filename='gmagik.gif')
			for image in glob.glob(gif_dir+"*_{0}.png".format(rand)):
				os.remove(image)
			os.remove(gifin)
			os.remove(gifout)
			await self.bot.delete_message(x)
		except Exception as e:
			print(e)

	#redacted
	@commands.command(pass_context=True)
	async def aa(self, ctx, *, user:str):
		"""rope"""
		user = user.strip("`")
		if len(ctx.message.mentions):
			user = ctx.message.mentions[0].name
		msg = "``` _________     \n|         |    \n|         0 <-- {0}    \n|        /|\\  \n|        / \\  \n|              \n|              \n```\n".format(user)
		msg += "**kronk your splinter** `{0}`\nropstor.org?u={1}".format(user, quote(user))    
		await ctx.send(msg)

	@commands.command(pass_context=True)
	async def a(self, ctx, *, user:str, direct=None):
		"""make dank meme"""
		if len(user) > 25:
			await ctx.send("ur names 2 long asshole")
			return
		if len(ctx.message.mentions) and len(ctx.message.mentions) == 1:
			user = ctx.message.mentions[0].name
		payload = {'template_id': '57570410', 'username': '', 'password' : '', 'text0' : '', 'text1' : '{0} you'.format(user)}
		with aiohttp.ClientSession() as session:
			async with session.post("https://api.imgflip.com/caption_image", data=payload) as r:
				load = await r.json()
		url = load['data']['url']
		if direct:
			await ctx.send(url)
		else:
			b = await self.bytes_download(url)
			await self.bot.upload(b, filename='a.png')

	@commands.command(pass_context=True)
	async def caption(self, ctx, url:str=None, text:str=None, color=None, size=None, x:int=None, y:int=None):
		"""Add caption to an image\n .caption text image_url"""
		try:
			if url is None:
				await ctx.send("Error: Invalid Syntax\n`.caption <image_url> <text>** <color>* <size>* <x>* <y>*`\n`* = Optional`\n`** = Wrap text in quotes`")
				return
			check = await self.isimage(url)
			if check == False:
				await ctx.send("Invalid or Non-Image!")
				return
			xx = await self.bot.send_message(ctx.message.channel, "ok, processing")
			b = await self.bytes_download(url)
			img = wand.image.Image(file=b)
			i = img.clone()
			font_path = self.files_path('impact.ttf')
			if size != None:
				color = wand.color.Color('{0}'.format(color))
				font = wand.font.Font(path=font_path, size=int(size), color=color)
			elif color != None:
				color = wand.color.Color('{0}'.format(color))
				font = wand.font.Font(path=font_path, size=40, color=color)
			else:
				color = wand.color.Color('red')
				font = wand.font.Font(path=font_path, size=40, color=color)
			if x is None:
				x = None
				y = int(i.height/10)
			if x != None and x > 250:
				x = x/2
			if y != None and y > 250:
				y = y/2
			if x != None and x > 500:
				x = x/4
			if y != None and y > 500:
				y = y/4
			if x != None:
				i.caption(str(text), left=x, top=y, font=font, gravity='center')
			else:
				i.caption(str(text), top=y, font=font, gravity='center')
			final = BytesIO()
			i.save(file=final)
			final.seek(0)
			await self.bot.delete_message(xx)
			await self.bot.upload(final, filename='caption.png')
		except Exception as e:
			await ctx.send("Error: Invalid Syntax\n `.caption <image_url> <text>** <color>* <size>* <x>* <y>*`\n`* = Optional`\n`** = Wrap text in quotes`")
			print(e)

	@commands.command(pass_context=True)
	async def triggered(self, ctx, user:str=None):
		"""Generate a Triggered Gif for a User or Image"""
		try:
			url = None
			if user is None:
				user = ctx.message.author
			elif len(ctx.message.mentions):
				user = ctx.message.mentions[0]
			else:
				url = user
			if type(user) == discord.User or type(user) == discord.Member:
				if user.avatar:
					avatar = 'https://discordapp.com/api/users/{0.id}/avatars/{0.avatar}.jpg'.format(user)
				else:
					avatar = user.default_avatar_url
			if url:
				get_images = await self.get_images(ctx, urls=url, limit=1)
				if not get_images:
					return
				avatar = get_images[0]
			path = self.files_path(self.bot.random(True))
			path2 = path[:-3]+'gif'
			await self.download(avatar, path)
			t_path = self.files_path('triggered.jpg')
			await self.bot.run_process(['convert',
				'canvas:none',
				'-size', '512x680!',
				'-resize', '512x680!',
				'-draw', 'image over -60,-60 640,640 "{0}"'.format(path),
				'-draw', 'image over 0,512 0,0 "{0}"'.format(t_path),
				'(',
					'canvas:none',
					'-size', '512x680!',
					'-draw', 'image over -45,-50 640,640 "{0}"'.format(path),
					'-draw', 'image over 0,512 0,0 "{0}"'.format(t_path),
				')',
				'(',
					'canvas:none',
					'-size', '512x680!',
					'-draw', 'image over -50,-45 640,640 "{0}"'.format(path),
					'-draw', 'image over 0,512 0,0 "{0}"'.format(t_path),
				')',
				'(',
					'canvas:none',
					'-size', '512x680!',
					'-draw', 'image over -45,-65 640,640 "{0}"'.format(path),
					'-draw', 'image over 0,512 0,0 "{0}"'.format(t_path),
				')',
				'-layers', 'Optimize',
				'-set', 'delay', '2',
			path2])
			await self.bot.upload(path2, filename='triggered.gif')
			os.remove(path)
			os.remove(path2)
		except Exception as e:
			await ctx.send(e)
			try:
				os.remove(path)
				os.remove(path2)
			except:
				pass

	async def do_triggered(self, ctx, user, url, t_path):
		try:
			if user is None:
				user = ctx.message.author
			elif len(ctx.message.mentions):
				user = ctx.message.mentions[0]
			else:
				url = user
			if type(user) == discord.User or type(user) == discord.Member:
				if user.avatar:
					avatar = 'https://discordapp.com/api/users/{0.id}/avatars/{0.avatar}.jpg'.format(user)
				else:
					avatar = user.default_avatar_url
			if url:
				get_images = await self.get_images(ctx, urls=url, limit=1)
				if not get_images:
					return
				avatar = get_images[0]
			path = self.files_path(self.bot.random(True))
			await self.download(avatar, path)
			await self.bot.run_process(['convert',
				'(',
					path,
					'-resize', '256', 
				')',
				t_path,
				'-append', path
			])
			return path
		except Exception as e:
			print(e)
			return False

	@commands.command(pass_context=True)
	async def triggered2(self, ctx, user:str=None, url:str=None):
		"""Generate a Triggered Image for a User or Image"""
		t_path = self.files_path('triggered.png')
		path = await self.do_triggered(ctx, user, url, t_path)
		if path is False:
			await ctx.send(':warning: **Command Failed.**')
			try:
				os.remove(path)
			except:
				pass
			return
		await self.bot.upload(path, filename='triggered3.png')
		os.remove(path)

	@commands.command(pass_context=True)
	async def triggered3(self, ctx, user:str=None, url:str=None):
		"""Generate a Triggered2 Image for a User or Image"""
		t_path = self.files_path('triggered2.png')
		path = await self.do_triggered(ctx, user, url, t_path)
		if path is False:
			await ctx.send(':warning: **Command Failed.**')
			try:
				os.remove(path)
			except:
				pass
			return
		await self.bot.upload(path, filename='triggered3.png')
		os.remove(path)

	@commands.command(pass_context=True, aliases=['aes'])
	async def aesthetics(self, ctx, *, text:str):
		"""Returns inputed text in aesthetics"""
		final = ""
		pre = ' '.join(text)
		for char in pre:
			if not ord(char) in range(33, 127):
				final += char
				continue
			final += chr(ord(char) + 65248)
		await self.truncate(ctx.message.channel, final)

	def do_ascii(self, text):
		try:
			i = PIL.Image.new('RGB', (2000, 1000))
			img = PIL.ImageDraw.Draw(i)
			txt = figlet_format(text, font='starwars')
			img.text((20, 20), figlet_format(text, font='starwars'), fill=(0, 255, 0))
			text_width, text_height = img.textsize(figlet_format(text, font='starwars'))
			imgs = PIL.Image.new('RGB', (text_width + 30, text_height))
			ii = PIL.ImageDraw.Draw(imgs)
			ii.text((20, 20), figlet_format(text, font='starwars'), fill=(0, 255, 0))
			text_width, text_height = ii.textsize(figlet_format(text, font='starwars'))
			final = BytesIO()
			imgs.save(final, 'png')
			final.seek(0)
			return final, txt
		except:
			return False, False

	@commands.command(pass_context=True, aliases=['expand'])
	async def ascii(self, ctx, *, text:str):
		"""Convert text into ASCII"""
		if len(text) > 1000:
			await ctx.send("2 long asshole")
			return
		if text == 'donger' or text == 'dong':
			text = "8====D"
		final, txt = await self.bot.loop.run_in_executor(None, self.do_ascii, text)
		if final is False:
			await ctx.send(':no_entry: go away with your invalid characters.')
			return
		if len(txt) >= 1999:
			await self.gist(ctx, text, txt)
			msg = None
		elif len(txt) <= 600:
			msg = "```fix\n{0}```".format(txt)
		else:
			msg = None
		await self.bot.upload(final, filename='ascii.png', content=msg)

	def generate_ascii(self, image):
		font = PIL.ImageFont.truetype(self.files_path('FreeMonoBold.ttf'), 15, encoding="unic")
		image_width, image_height = image.size
		aalib_screen_width= int(image_width/24.9)*10
		aalib_screen_height= int(image_height/41.39)*10
		screen = aalib.AsciiScreen(width=aalib_screen_width, height=aalib_screen_height)
		im = image.convert("L").resize(screen.virtual_size)
		screen.put_image((0,0), im)
		y = 0
		how_many_rows = len(screen.render().splitlines()) 
		new_img_width, font_size = font.getsize(screen.render().splitlines()[0])
		img = PIL.Image.new("RGBA", (new_img_width, how_many_rows*15), (255,255,255))
		draw = PIL.ImageDraw.Draw(img)
		for lines in screen.render().splitlines():
			draw.text((0,y), lines, (0,0,0), font=font)
			y = y + 15
		imagefit = PIL.ImageOps.fit(img, (image_width, image_height), PIL.Image.ANTIALIAS)
		return imagefit

	@commands.command(pass_context=True)
	async def iascii(self, ctx, url:str=None):
		try:
			get_images = await self.get_images(ctx, urls=url, limit=5)
			if not get_images:
				return
			for url in get_images:
				x = await ctx.send("ok, processing")
				b = await self.bytes_download(url)
				if b is False:
					if len(get_images) == 1:
						await ctx.send(':warning: **Command download function failed...**')
						return
					continue
				im = PIL.Image.open(b)
				img = await self.bot.loop.run_in_executor(None, self.generate_ascii, im)
				final = BytesIO()
				img.save(final, 'png')
				final.seek(0)
				await self.bot.delete_message(x)
				await self.bot.upload(final, filename='iascii.png')
		except Exception as e:
			await ctx.send(e)

	def do_gascii(self, b, rand, gif_dir):
		try:
			try:
				im = PIL.Image.open(b)
			except IOError:
				return ':warning: Cannot load gif.'
			count = 0
			mypalette = im.getpalette()
			try:
				while True:
					im.putpalette(mypalette)
					new_im = PIL.Image.new("RGBA", im.size)
					new_im.paste(im)
					new_im = self.generate_ascii(new_im)
					new_im.save('{0}/{1}_{2}.png'.format(gif_dir, count, rand))
					count += 1
					im.seek(im.tell() + 1)
				return True
			except EOFError:
				pass
		except Exception as e:
			print(e)

	@commands.command(pass_context=True)
	async def gascii(self, ctx, url:str=None):
		"""Gif to ASCII"""
		try:
			get_images = await self.get_images(ctx, urls=url, gif=True, limit=2)
			if not get_images:
				await ctx.send("Error: Invalid Syntax\n`.gascii <gif_url> <liquid_rescale>*`\n`* = Optional`")
				return
			for url in get_images:
				rand = self.bot.random()
				gif_dir = self.files_path('gascii/')
				location = gif_dir+'1_{0}.gif'.format(rand)
				location2 = gif_dir+'2_{0}.gif'.format(rand)
				x = await self.bot.send_message(ctx.message.channel, "ok, processing")
				await self.download(url, location)
				if os.path.getsize(location) > 3000000 and ctx.message.author.id != self.bot.owner.id:
					await ctx.send("Sorry, GIF Too Large!")
					os.remove(location)
					return
				result = await self.bot.loop.run_in_executor(None, self.do_gascii, location, rand, gif_dir)
				if type(result) == str:
					await ctx.send(result)
					return
				list_imgs = glob.glob(gif_dir+"*_{0}.png".format(rand))
				if len(list_imgs) > 120 and ctx.message.author.id != "130070621034905600":
					await ctx.send("Sorry, GIF has too many frames!")
					for image in list_imgs:
						os.remove(image)
					os.remove(location)
					return
				await self.bot.run_process(['ffmpeg', '-y', '-nostats', '-loglevel', '0', '-i', self.files_path('gascii/')+'%d_{0}.png'.format(rand), location2])
				await self.bot.delete_message(x)
				await self.bot.upload(location2, filename='gascii.gif')
				for image in list_imgs:
					os.remove(image)
				os.remove(location)
				os.remove(location2)
		except Exception as e:
			await ctx.send(e)

	@commands.command(pass_context=True)
	async def rip(self, ctx, name:str=None, *, text:str=None):
		if name is None:
			name = ctx.message.author.name
		if len(ctx.message.mentions) >= 1:
			name = ctx.message.mentions[0].name
		if text != None:
			if len(text) > 22:
				one = text[:22]
				two = text[22:]
				url = "http://www.tombstonebuilder.com/generate.php?top1=R.I.P&top3={0}&top4={1}&top5={2}".format(name, one, two).replace(" ", "%20")
			else:
				url = "http://www.tombstonebuilder.com/generate.php?top1=R.I.P&top3={0}&top4={1}".format(name, text).replace(" ", "%20")
		else:
			if name[-1].lower() != 's':
				name += "'s"
			url = "http://www.tombstonebuilder.com/generate.php?top1=R.I.P&top3={0}&top4=Hopes and Dreams".format(name).replace(" ", "%20")
		b = await self.bytes_download(url)
		await self.bot.upload(b, filename='rip.png')

#	@commands.command(pass_context=True)
#	async def urban(self, ctx, *, word:str):
#		urb = urbandict.define(word)
#		if "There aren't any definitions" in urb[0]['def']:
#			await ctx.send(":no_mouth: `No definition found.`")
#			return
#		msg = "**{0}**\n".format(word)
#		msg += "`Definition:` {0}\n".format(urb[0]['def'].replace("\n", ""))
#		msg += "`Example:` {0}".format(urb[0]['example'].replace("\n", ""))
#		await self.truncate(ctx.message.channel, msg)

	async def add_cache(self, search, result, t=0, level=1):
		try:
			try:
				if result['error']:
					return
			except KeyError:
				pass
			if t == 0:
				self.image_cache[search] = [result, level]
			elif t == 1:
				self.search_cache[search] = [result, level]
			elif t == 2:
				self.youtube_cache[search] = [result, level]
		except Exception as e:
			print(e)

	async def google_scrap(self, search:str, safe=True, image=False):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0'}
		search = quote(search)
		try:
			if image:
				api = 'https://www.google.com/search?tbm=isch&gs_l=img&safe={0}&q={1}'.format('on' if safe else 'off', search)
				with aiohttp.ClientSession() as session:
					with aiohttp.Timeout(5):
						async with session.get(api, headers=headers) as r:
							assert r.status == 200
							txt = await r.text()
				match = self.scrap_regex.findall(txt)
				assert match
				image = random.choice(match[:10])
				check = await self.isimage(image)
				i = 0
				if not check:
					while not check and i != 10:
						image = match[:10][i]
						check = await self.isimage(image)
						i += 1
				assert check
				return image
			else:
				api = 'https://www.google.com/search?safe={0}&q={1}'.format('on' if safe else 'off', search)
				#why are you so good danny, my old method was using regex so, not so good.....
				entries = {}
				with aiohttp.ClientSession() as session:
					with aiohttp.Timeout(5):
						async with session.get(api, headers=headers) as r:
							assert r.status == 200
							txt = await r.text()
				root = etree.fromstring(txt, etree.HTMLParser())
				search_nodes = root.findall(".//div[@class='g']")
				result = False
				for node in search_nodes:
					if result != False:
						break
					try:
						url_node = node.find('.//h3/a')
						if url_node is None:
							continue
						desc = get_deep_text(node.find(".//div[@class='s']/div/span[@class='st']"))
						title = get_deep_text(node.find(".//h3[@class='r']"))
						url = url_node.attrib['href']
						if url.startswith('/url?'):
							url = parse_qs(url[5:])['q'][0]
						result = [title, desc, url]
					except:
						continue
				return result
		except AssertionError:
			return False
		except Exception as e:
			print(e)
			return False

	async def google_safety(self, message, s=False):
		check = await self.is_nsfw(message)
		if check:
			if s:
				return 'off'
			return 1, False
		sql = 'SELECT * FROM `google_nsfw` WHERE server={0}'
		sql = sql.format(message.server.id)
		result = self.cursor.execute(sql).fetchall()
		if len(result) == 0:
			if s:
				return 'medium'
			return 2, False
		else:
			level = int(result[0]['level'])
			if s:
				if level == 1:
					return 'off'
				elif level == 2:
					return 'medium'
				elif level == 3:
					return 'high'
			return level

	@commands.command(pass_context=True, aliases=['googlesafety', 'safetylevel', 'googlensfw', 'saftey'])
	async def safety(self, ctx, level:str=None):
		s = await self.google_safety(ctx.message)
		current_level = s[0] if type(s) != str and type(s) != int else s
		check = s[1] if type(s) != str and type(s) != int else True
		levels = [0, 1, 2, 3]
		if current_level == 1:
			msg = 'OFF'
		elif current_level == 2:
			msg = 'MEDIUM'
		elif current_level == 3:
			msg = 'HIGH'
		if level is None:
			await ctx.send(':information_source: Current google safety level: `{0}` *{1}*'.format(current_level, msg))
			return
		else:
			level = level.lower()
			if level.isdigit() and int(level) in levels:
				level = int(level)
			elif level == 'off' or level == 'disable':
				level = 1
			elif level == 'low' or level == 'medium':
				level = 2
			elif level == 'high':
				level = 3
			if level not in levels:
				await ctx.send(':no_entry: `Invalid level.`')
				return
		if level == 0 or level == 1:
			level = 1
			smsg = 'OFF'
		elif level == 2:
			smsg = 'MEDIUM'
		elif level == 3:
			smsg = 'HIGH'
		if current_level == level:
			await ctx.send(':no_entry: Google Saftey is already at that level!')
			return
		if check is False:
			sql = 'INSERT INTO `google_nsfw` (`server`, `level`) VALUES (%s, %s)'
			self.cursor.execute(sql, (ctx.message.server.id, level))
			await ctx.send(':white_check_mark: Set google safety level to **{1}**'.format(level, smsg))
		else:
			sql = 'UPDATE `google_nsfw` SET level={0} WHERE server={1}'
			sql = sql.format(level, ctx.message.server.id)
			self.cursor.execute(sql)
			await ctx.send(':white_check_mark: Updated google safety level from **{0}** *to* **{1}**'.format(msg, smsg))
		self.cursor.commit()

	@commands.command(pass_context=True, aliases=['im', 'photo', 'img'])
	async def image(self, ctx, *, search:str):
		level = await self.google_safety(ctx.message, True)
		in_cache = False
		if search in self.image_cache.keys():
			load_level = self.image_cache[search][1]
			if load_level == level:
				load = self.image_cache[search][0]
				in_cache = True
		try:
			if in_cache is False:
				key = await self.google_keys()
				api = "https://www.googleapis.com/customsearch/v1?key={0}&cx=015418243597773804934:it6asz9vcss&searchType=image&safe={1}&q={2}".format(key, level, quote(search))
				load = await self.get_json(api)
				assert 'error' not in load.keys() and 'items' in load.keys()
				assert len(load)
			rand = random.choice(load['items'])
			image = rand['link']
			await ctx.send(image)
			await self.add_cache(search, load, 0, level)
		except discord.errors.Forbidden:
			await ctx.send("no send_file permission asshole")
			return
		except AssertionError:
			scrap = await self.google_scrap(search, True if level != 'off' else False, True)
			if scrap:
				await ctx.send(scrap)
			else:
				await ctx.send(":warning: `API Quota Reached or Invalid Search`")
		except:
			raise

	@commands.command(pass_context=True, aliases=['go', 'googl', 'gogle', 'g'])
	async def google(self, ctx, *, search:str=None):
		if search is None:
			await ctx.send("Error: Invalid Syntax\n`.google <text>`")
			return
		in_cache = False
		level = await self.google_safety(ctx.message, True)
		in_cache = False
		if search in self.search_cache.keys():
			load_level = self.search_cache[search][1]
			if load_level == level:
				load = self.search_cache[search][0]
				in_cache = True
		try:
			if in_cache is False:
				key = await self.google_keys()
				api = "https://www.googleapis.com/customsearch/v1?key={0}&cx=015418243597773804934:it6asz9vcss&safe={1}&q={2}".format(key, level, quote(search))
				load = await self.get_json(api)
				assert 'error' not in load.keys() and 'items' in load.keys()
				assert len(load)
			rand = load['items'][0]
			result = rand['link']
			title = rand['title']
			snippet = rand['snippet']
			await ctx.send("**{0}**\n`{1}`\n{2}".format(title, snippet, result))
			await self.add_cache(search, load, 1, level)
		except AssertionError:
			scrap = await self.google_scrap(search, True if level != 'off' else False, False)
			if scrap:
				title = scrap[0]
				snippet = scrap[1]
				result = scrap[2]
				await ctx.send("**{0}**\n`{1}`\n{2}".format(title, snippet, result))
			else:
				await ctx.send(":warning: `API Quota Reached or Invalid Search`")
		except:
			raise

	async def youtube_scrap(self, search:str, safety=False):
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0'}
		search = quote(search)
		api = 'https://www.youtube.com/results?search_query={0}'.format(search)
		entries = {}
		cookies = {'PREF': 'cvdm=grid&al=en&f4=4000000&f5=30&f1=50000000&f2=8000000'} if safety else None
		with aiohttp.ClientSession(cookies=cookies) as session:
			with aiohttp.Timeout(5):
				async with session.get(api, headers=headers) as r:
					assert r.status == 200
					txt = await r.text()
		root = etree.fromstring(txt, etree.HTMLParser())
		search_nodes = root.findall(".//ol[@class='section-list']/li/ol[@class='item-section']/li")
		if len(search_nodes) == 0:
			return False
		search_nodes.pop(0)
		result = False
		for node in search_nodes:
			if result != False:
				break
			try:
				url_node = node.find('div/div/div/h3/a')
				if url_node is None:
					continue
				title = get_deep_text(url_node)
				url = 'https://www.youtube.com/{0}'.format(url_node.attrib['href'])
				result = [title, url]
			except:
				continue
		return result

	@commands.command(pass_context=True, aliases=['yt', 'video'])
	async def youtube(self, ctx, *, search:str=None):
		if search is None:
			await ctx.send("Error: Invalid Syntax\n`.yt/youtube <text>`")
			return
		level = await self.google_safety(ctx.message, True)
		in_cache = False
		if search in self.youtube_cache.keys():
			load_level = self.youtube_cache[search][1]
			if load_level == level:
				load = self.youtube_cache[search][0]
				in_cache = True
		try:
			if in_cache is False:
				key = await self.google_keys()
				api = "https://www.googleapis.com/customsearch/v1?key={0}&cx=015418243597773804934:cdlwut5fxsk&q={1}".format(key, quote(search))
				load = await self.get_json(api)
				assert 'error' not in load.keys() and 'items' in load.keys()
				assert len(load)
			rand = load['items'][0]
			link = rand['link']
			title = rand['title']
			snippet = rand['snippet']
			await ctx.send('**{0}**\n`{1}`\n{2}'.format(title, snippet, link))
			await self.add_cache(search, load, 2, level)
		except AssertionError:
			scrap = await self.youtube_scrap(search, True if level != 'off' else False)
			if scrap:
				title = scrap[0]
				url = scrap[1]
				await ctx.send("**{0}**\n{1}".format(title, url))
			else:
				await ctx.send(":warning: `API Quota Reached or Invalid Search`")

	@commands.command()
	async def imgur(self, *, text:str=None):
		try:
			if text is None:
				load = self.imgur_client.gallery_random(page=0)
			else:
				load = self.imgur_client.gallery_search(text, advanced=None, sort='viral', window='all', page=0)
			rand = random.choice(load)
			try:
				if 'image/' in rand.type:
					await ctx.send('{0}'.format(rand.link))
			except AttributeError:
				if rand.title:
					title = '**'+rand.title+'**\n'
				else:
					title = ''
				if rand.description != None:
					desc = '`'+rand.description+'`\n'
				else:
					desc = ''
				await ctx.send('{0}{1}{2}'.format(title, desc, rand.link))
		except Exception as e:
			await ctx.send(e)

	@commands.command(aliases=['gif'])
	async def giphy(self, *, text:str=None):
		if text is None:
			api = 'http://api.giphy.com/v1/gifs/random?&api_key=dc6zaTOxFJmzC'
		else:
			api = 'http://api.giphy.com/v1/gifs/search?q={0}&api_key=dc6zaTOxFJmzC'.format(quote(text))
		load = await self.get_json(api)
		if len(load['data']) == 0:
			await ctx.send(':warning: `No results found on` <https://giphy.com>')
		else:
			rand = False
			try:
				gif = random.choice(load['data'])
			except:
				gif = load['data']
				rand = True
			url = gif['url']
			if rand:
				gif_url = gif['image_url']
			else:
				gif_url = gif['images']['fixed_height']['url']
			await ctx.send('{0}'.format(url))

	@commands.command(pass_context=True, aliases=['w2x', 'waifu2x', 'enlarge', 'upscale'])
	async def resize(self, ctx, *urls):
		try:
			get_images = await self.get_images(ctx, urls=urls, scale=10, limit=1)
			if not get_images:
				return
			url = get_images[0][0]
			size = get_images[1]
			if size is None:
				size = 3
			scale_msg = get_images[2]
			if scale_msg is None:
				scale_msg = ''
			else:
				scale_msg = '\n'+scale_msg
			do_2 = False
			rand = self.bot.random()
			x = await self.bot.send_message(ctx.message.channel, "ok, resizing `{0}` by `{1}`".format(url, str(size)))
			b = await self.bytes_download(url)
			if sys.getsizeof(b) > 3000000:
				await ctx.send("Sorry, image too large for waifu2x servers!")
				return
			await self.bot.edit_message(x, "25%, resizing")
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0'}
			payload = aiohttp.FormData()
			payload.add_field('url', url)
			payload.add_field('scale', str(size))
			payload.add_field('style', 'art')
			payload.add_field('noise', '3')
			payload.add_field('comp', '10')
			await self.bot.edit_message(x, "50%, w2x")
			try:
				with aiohttp.ClientSession() as session:
					with aiohttp.Timeout(30):
						async with session.post('http://waifu2x.me/convert', data=payload, headers=headers) as r:
							txt = await r.text()
				download_url = 'http://waifu2x.me/{0}'.format(txt)
				final = None
			except asyncio.TimeoutError:
				do_2 = True
			if do_2:
				idk = []
				if size == 1:
					idk.append(2)
				if size == 2:
					idk.append(2)
				if size == 3:
					idk.append(1.6)
					idk.append(2)
				if size == 4:
					idk.append(2)
					idk.append(2)
				if size == 5:
					idk.append(1.6)
					idk.append(2)
					idk.append(2)
				if size == 6:
					for i in range(3):
						idk.append(2)
				if size == 7:
					for i in range(3):
						idk.append(2)
					idk.append(1.6)
				if size == 8:
					for i in range(4):
						idk.append(2)
				if size == 9:
					for i in range(4):
						idk.append(2)
					idk.append(1.6)
				if size == 10:
					for i in range(5):
						idk.append(2)
				for s in idk:
					if final:
						b = final
					if s == 2:
						headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0'}
						payload = aiohttp.FormData()
						payload.add_field('scale', '2')
						payload.add_field('style', 'art')
						payload.add_field('noise', '1')
						payload.add_field('url', url)
						with aiohttp.ClientSession() as session:
							with aiohttp.Timeout(30):
								async with session.post('http://waifu2x.udp.jp/api', data=payload, headers=headers) as r:
									raw = await r.read()
					elif s == 1.6:
						headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0'}
						payload = aiohttp.FormData()
						payload.add_field('scale', '1.6')
						payload.add_field('style', 'art')
						payload.add_field('noise', '1')
						payload.add_field('url', url)
						with aiohttp.ClientSession() as session:
							with aiohttp.Timeout(30):
								async with session.post('http://waifu2x.udp.jp/api', data=payload, headers=headers) as r:
									raw = await r.read()
					final = BytesIO(raw)
					final.seek(0)
			if final is None:
				final = await self.bytes_download(download_url)
			if sys.getsizeof(final) > 8388608:
				await ctx.send("Sorry, image too large for discord!")
				return
			await self.bot.edit_message(x, "100%, uploading")
			i = 0
			while sys.getsizeof(final) == 88 and i < 5:
				final = await self.bytes_download(download_url)
				await asyncio.sleep(0.3)
				if sys.getsizeof(final) != 0:
					i = 5
				else:
					i += 1
			await self.bot.upload(final, filename='enlarge.png', content='Visit image link for accurate resize visual.'+scale_msg if size > 3 else scale_msg if scale_msg != '' else None)
			await asyncio.sleep(3)
			await self.bot.delete_message(x)
		except Exception as e:
			await ctx.send(code.format(e))
			await ctx.send("Error: Failed\n `Discord Failed To Upload or Waifu2x Servers Failed`")

	@commands.group(pass_context=True, invoke_without_command=True)
	async def meme(self, ctx, meme:str=None, *, line=None):
		"""Generates a meme."""
		if meme is None:
			await ctx.send("Error: Invalid Syntax\n`meme` has 4 commands\n`meme` **+** `<mention> or <custom_image> or <template>` **+** `<line1> <line2>*` *=optional")
			return
		if line is None:
			await ctx.send("Error: Invalid Syntax\n`meme` has 4 parameters\n`.meme <template> <line_one> <line_two> <style>*`\n* = Optional")
			return
		line2 = None
		if '|' in line:
			split = line.split('|')
			line1 = split[0]
			line2 = split[1]
		else:
			split = line.split()
			if len(split) > 2:
				line1 = ' '.join(split[:2])
				line2 = ' '.join(split[2:])
			else:
				line1 = split[0]
				if len(split) > 1:
					line2 = ' '.join(split[1:])
		if line2 is None:
			line2 = ''
		rep = [["-","--"],["_","__"],["?","~q"],["%","~p"],[" ","%20"],["''","\""]]
		for s in rep:
			line1 = line1.replace(s[0],s[1])
			line2 = line2.replace(s[0],s[1])
		if len(ctx.message.mentions):
			link = "http://memegen.link/custom/{0}/{1}.jpg?alt={2}".format(line1, line2, 'https://discordapp.com/api/users/{0.id}/avatars/{0.avatar}.jpg'.format(ctx.message.mentions[0]))
			b = await self.bytes_download(link)
		elif meme.startswith("http"):
			link = "http://memegen.link/custom/{0}/{1}.jpg?alt={2}".format(line1, line2, meme)
			b = await self.bytes_download(link)
		else:
			link = "http://memegen.link/{0}/{1}/{2}.jpg".format(meme, line1, line2)
			b = await self.bytes_download(link)
		if b is False:
			await ctx.send(':warning: **Command download function failed...**')
			return
		await self.bot.upload(b, filename='meme.png')

	@meme.group(name="templates", pass_context=True, invoke_without_command=True)
	async def _templates(self, ctx):
		"""Gives users a list of meme templates."""
		await ctx.send("Templates to choose from: <{}>".format("http://memegen.link/templates/"))

#	@commands.command(aliases=['r'])
#	async def reverse(self, *, text:str):
#		"""Reverse Text\n.revese <text>"""
#		text = text.replace('\u202E', '')
#		s = text.split('\n')
#		kek = ''
#		for x in s:
#			kek += u"\u202E " + x + '\n'
#		kek = kek
#		await ctx.send(kek, replace_mentions=True)

	async def get_emote_image(self, em, one=False, apple=False):
		em = em.replace('⠀', '').replace(' ', '')
		emote = em.lower()
		emote = emote.encode("unicode_escape").decode()
		if "\\U000" in emote and emote.count("\\U000") == 1:
			emote = emote.replace("\\U000", '')
		elif emote.count("\\U000") == 2:
			emote = emote.split("\\U000")
			emote = '{0}-{1}'.format(emote[1], emote[2])
		else:
			emote = emote.replace("\\u", '')
		if em == '🏳️‍🌈':
			emote = '1f308'
		if one:
			path = self.files_path('emojione/{0}.svg'.format(emote))
		elif apple:
			path = self.files_path('apple_emoji/{0}.png'.format(emote))
		else:
			path = self.files_path('twemoji/{0}.svg'.format(emote))
		return path

	async def png_svg(self, path, size):
		with open(path, 'rb') as f:
			path = f.read()
		s = bytes(str(size), encoding="utf-8")
		b = path.replace(b"<svg ", b"<svg width=\"" + s + b"px\" height=\"" + s + b"px\" ")
		path = BytesIO(cairosvg.svg2png(b))
		return path

	fp_emotes = {
		#redacted spam
	}
	@commands.command(pass_context=True, aliases=['hugemoji', 'hugeemoji'])
	async def e(self, ctx, *ems:str):
		"""Returns a large emoji image"""
		try:
			if len(ems) == 0:
				await ctx.send(':no_entry: Please input emotes to enlargen.')
				return
			if len(ems) > 50:
				await ctx.send(':no_entry: `Max emoji limit (<= 50)`')
				return
			size = 1024
			for s in ems:
				if s.isdigit():
					size = int(s)
			if size > 2048:
				size = 2048
			one = False
			apple_emote = False
			steam = False
			for em in ems:
				if em == 'emojione' or em == 'one':
					one = True
				elif em == 'apple' or em == 'ios':
					apple_emote = True
				elif em == 'steam':
					steam = True
			if len(self.twitch_cache) == 0:
				twitch_images_load = await self.get_json('https://twitchemotes.com/api_cache/v2/images.json')
				twitch_sub_load = await self.get_json('https://twitchemotes.com/api_cache/v2/subscriber.json')
				self.twitch_cache.append(twitch_images_load)
				self.twitch_cache.append(twitch_sub_load)
			else:
				twitch_images_load = self.twitch_cache[0]
				twitch_sub_load = self.twitch_cache[1]
			list_imgs = []
			count = -1
			for em in ems:
				if em == 'emojione' or em == 'one' or em == 'apple' or em == 'ios' or em == 'steam':
					continue
				if str(em).isdigit():
					continue
				if em == ' ' or em == '​':
					continue
				found = False
				gif = False
				count += 1
				path = await self.get_emote_image(em, one, apple_emote)
				if os.path.isfile(path) is False:
					match = self.emote_regex.match(ems[count])
					if match != None:
						emote = 'https://cdn.discordapp.com/emojis/{0}.png'.format(str(match.group('id')))
						path = await self.bytes_download(emote)
						if sys.getsizeof(path) == 88:
							continue
						else:
							found = True
				else:
					found = True
					if not apple_emote:
						path = await self.png_svg(path, size)
				if not found:
					match = em.strip(':')
					if match in self.fp_emotes:
						found = True
						url = self.fp_emotes[match]
						path = await self.bytes_download(url)
				if not found:
					match = em.strip(':')
					if match in [x[:-4] for x in self.fp_dir]:
						try:
							f = self.fp_dir[self.fp_dir.index(match+'.png')]
						except:
							f = self.fp_dir[self.fp_dir.index(match+'.gif')]
							gif = True
						found = True
						path = self.files_path('fp/{0}'.format(f))
				if not found:
					frankerz_path = self.files_path('frankerz_emotes.txt')
					frankerz_emotes = []
					with open(frankerz_path) as f:
						for line in f:
							frankerz_emotes.append(json.loads(line))
						f.close()
					for page in frankerz_emotes:
						for emote in page['emoticons']:
							if emote['name'] == em:
								found = True
								try:
									url = 'https:'+emote['urls']['4']
								except:
									try:
										url = 'https:'+emote['urls']['3']
									except:
										try:
											url = 'https:'+emote['urls']['2']
										except:
											url = 'https:'+emote['urls']['1']
								path = await self.bytes_download(url)
								break
					if not found:
						load = twitch_images_load
						for emote in load['images']:
							if load['images'][emote]['code'] == em:
								found = True
								url = 'https://static-cdn.jtvnw.net/emoticons/v1/{0}/3.0'.format(emote)
								path = await self.bytes_download(url)
								break
					if not found:
						load = twitch_sub_load
						for channel in load['channels']:
							for emote in load['channels'][channel]['emotes']:
								if emote['code'] == em:
									found = True
									url = 'https://static-cdn.jtvnw.net/emoticons/v1/{0}/3.0'.format(emote)
									path = await self.bytes_download(url)
									break
					if not found:
						if em in self.emojis.keys():
							path = await self.png_svg(await self.get_emote_image(self.emojis[em]), size)
							found = True
					if not found and steam:
						steam_url = "https://steamcommunity-a.akamaihd.net/economy/emoticon/{0}".format(em.lower())
						s_e = await self.bytes_download(steam_url)
						if sys.getsizeof(s_e) != 88:
							path = s_e
							found = True
				if found:
					list_imgs.append(path)
			if len(list_imgs) == 0:
				if ems:
					for s in ems:
						for w in s:
							if w in alphabet:
								list_imgs.append(await self.png_svg(await self.get_emote_image(self.regional_map[w]), size))
				if not list_imgs:
					em = [e for e in em]
					path = await self.get_emote_image(em[0])
					if os.path.isfile(path):
						for e in em:
							path = await self.get_emote_image(e)
							if os.path.isfile(path):
								list_imgs.append(await self.png_svg(path, size))
				if not list_imgs:
					await ctx.send(":warning: `Emoji Invalid/Not Found`")
					return
			if len(list_imgs) > 1:
				imgs = [PIL.Image.open(i).convert('RGBA') for i in list_imgs]
				min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
				imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
				imgs_comb = PIL.Image.fromarray(imgs_comb)
				b = BytesIO()
				imgs_comb.save(b, 'png')
				b.seek(0)
			else:
				b = list_imgs[0]
			try:
				await self.bot.upload(b, filename='emote.gif' if gif and len(list_imgs) == 1 else 'emote.png')
			except:
				await ctx.send('sorry, file 2 big (> 8 mb)')
			await asyncio.sleep(5)
			try:
				self.bot.pruned_messages.append(ctx.message)
				await self.bot.delete_message(ctx.message)
			except:
				pass
		except Exception as e:
			exc_type, exc_obj, tb = sys.exc_info()
			f = tb.tb_frame
			lineno = tb.tb_lineno
			filename = f.f_code.co_filename
			linecache.checkcache(filename)
			line = linecache.getline(filename, lineno, f.f_globals)
			await ctx.send(code.format('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)))

	@commands.command(pass_context=True, aliases=['steamemoji', 'steame', 'semoji'])
	async def se(self, ctx, em:str):
		"""Returns a steam emoji image"""
		em = em.lower()
		desc = None
		if em == ':b1:' or em == 'b1':
			b = self.files_path('b1.png')
		else:
			url = "https://steamcommunity-a.akamaihd.net/economy/emoticonhover/{0}".format(em)
			txt = await self.get_text(url)
			if not txt:
				await ctx.send(":warning: `Emoticon Not Found/Invalid`\nRemember to do :steam_emoticon: (optional ':').")
				return
			root = etree.fromstring(txt, etree.HTMLParser())
			base = root.find('.//img[@class="emoticon_large"]')
			b = BytesIO(base64.b64decode(base.attrib['src'][22:]))
			desc = '**{0}**'.format(root.find('.//div[@class="emoticon_hover_desc"]').text)
		await self.bot.upload(b, filename='steam.png', content=desc)

	@commands.command(pass_context=True)
	async def b1(self, ctx):
		"""cool"""
		await self.bot.upload(self.files_path('b1.png'))

	@commands.group(pass_context=True, invoke_without_command=True)
	async def merge(self, ctx, *urls:str):
		"""Merge/Combine Two Photos"""
		try:
			if urls and 'vertical' in urls:
				vertical = True
			else:
				vertical = False
			get_images = await self.get_images(ctx, urls=urls, limit=20)
			if get_images and len(get_images) == 1:
				await ctx.send('You gonna merge one image?')
				return
			elif not get_images:
				return
			xx = await self.bot.send_message(ctx.message.channel, "ok, processing")
			count = 0
			list_im = []
			for url in get_images:
				count += 1
				b = await self.bytes_download(url)
				if sys.getsizeof(b) == 215:
					await ctx.send(":no_entry: Image `{0}` is invalid!".format(str(count)))
					continue
				list_im.append(b)
			imgs = [PIL.Image.open(i).convert('RGBA') for i in list_im]
			if vertical:
				max_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[1][1]
				imgs_comb = np.vstack((np.asarray(i.resize(max_shape)) for i in imgs))
			else:
				min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
				imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
			imgs_comb = PIL.Image.fromarray(imgs_comb)
			final = BytesIO()
			imgs_comb.save(final, 'png')
			final.seek(0)
			await self.bot.delete_message(xx)
			await self.bot.upload(final, filename='merge.png')
		except Exception as e:
			await ctx.send(code.format(e))

	@commands.command(pass_context=True, aliases=['cancerify', 'em'])
	async def emojify(self, ctx, *, txt:str):
		txt = txt.lower()
		msg = ""
		for s in txt:
			if s in self.emoji_map:
				msg += "{0}".format(self.emoji_map[s])
			else:
				msg += s
		await ctx.send(msg)

	@commands.command(pass_context=True, aliases=['toe', 'analyze'])
	async def tone(self, ctx, *, text:str):
		"""Analyze Tone in Text"""
		payload = {'text':text}
		headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0.2 Waterfox/46.0.2'}
		with aiohttp.ClientSession() as session:
			async with session.post('https://tone-analyzer-demo.mybluemix.net/api/tone', data=payload, headers=headers) as r:
				load = await r.json()
		anger = load['document_tone']['tone_categories'][0]['tones'][0]['score']
		disgust = load['document_tone']['tone_categories'][0]['tones'][1]['score']
		fear = load['document_tone']['tone_categories'][0]['tones'][2]['score']
		joy = load['document_tone']['tone_categories'][0]['tones'][3]['score']
		sadness = load['document_tone']['tone_categories'][0]['tones'][4]['score']
		emotions_msg = "Anger: {0}\nDisgust: {1}\nFear: {2}\nJoy: {3}\nSadness: {4}".format(anger, disgust, fear, joy, sadness)
		analytical = load['document_tone']['tone_categories'][1]['tones'][0]['score']
		confident = load['document_tone']['tone_categories'][1]['tones'][1]['score']
		tentative = load['document_tone']['tone_categories'][1]['tones'][2]['score']
		language_msg = "Analytical: {0}\nConfidence: {1}\nTentitive: {2}".format(analytical, confident, tentative)
		openness = load['document_tone']['tone_categories'][2]['tones'][0]['score']
		conscientiousness = load['document_tone']['tone_categories'][2]['tones'][1]['score']
		extraversion = load['document_tone']['tone_categories'][2]['tones'][2]['score']
		agreeableness = load['document_tone']['tone_categories'][2]['tones'][3]['score']
		emotional_range = load['document_tone']['tone_categories'][2]['tones'][4]['score']
		social_msg = "Openness: {0}\nConscientiousness: {1}\nExtraversion (Stimulation): {2}\nAgreeableness: {3}\nEmotional Range: {4}".format(openness, conscientiousness, extraversion, agreeableness, emotional_range)
		await ctx.send("\n**Emotions**"+code.format(emotions_msg)+"**Language Style**"+code.format(language_msg)+"**Social Tendencies**"+code.format(social_msg))

	@commands.command(pass_context=True, aliases=['text2img', 'texttoimage', 'text2image'])
	async def tti(self, ctx, *, txt:str):
		api = 'http://api.img4me.com/?font=arial&fcolor=FFFFFF&size=35&type=png&text={0}'.format(quote(txt))
		r = await self.get_text(api)
		b = await self.bytes_download(r)
		await self.bot.upload(b, filename='tti.png')

	@commands.command(pass_context=True, aliases=['comicsans'])
	async def sans(self, ctx, *, txt:str):
		api = 'http://api.img4me.com/?font=sans&fcolor=000000&size=35&type=png&text={0}'.format(quote(txt))
		r = await self.get_text(api)
		b = await self.bytes_download(r)
		await self.bot.upload(b, filename='tti.png')

	@commands.command(pass_context=True, aliases=['needsmorejpeg', 'jpegify', 'magik2'])
	async def jpeg(self, ctx, url:str=None, quality:int=1):
		"""Add more JPEG to an Image\nNeeds More JPEG!"""
		if quality > 10:
			quality = 10
		elif quality < 1:
			quality = 1
		get_images = await self.get_images(ctx, urls=url)
		if not get_images:
			return
		for url in get_images:
			b = await self.bytes_download(url)
			if b is False:
				if len(get_images) == 1:
					await ctx.send(':warning: **Command download function failed...**')
					return
				continue
			img = PIL.Image.open(b).convert('RGB')
			final = BytesIO()
			img.save(final, 'JPEG', quality=quality)
			final.seek(0)
			await self.bot.upload(final, filename='needsmorejpeg.jpg')

	# @commands.command(pass_context=True, aliases=['needsmorejpeg', 'nmj', 'jpegify'])
	# async def jpeg(self, ctx, url:str, amount:int=5):
	# 	"""Add more JPEG to an Image\nNeeds More JPEG!"""
	# 	if url.startswith('<@') and len(ctx.message.mentions) != 0:
	# 		url = ctx.message.mentions[0].avatar_url
	# 	api = 'http://api.jpeg.li/v1/existing'
	# 	for x in amount:
	# 		payload = {
	# 			'url': url
	# 		}
	# 		r = requests.post(api, data=payload)
	# 		url = r.json()['url']
	# 	b = await self.bytes_download(url)
	# 	await self.bot.upload(b, filename='needsmorejpeg.jpg')

	def do_vw(self, b, txt):
		im = PIL.Image.open(b)
		k = random.randint(0, 100)
		im = macintoshplus.draw_method1(k, txt, im)
		final = BytesIO()
		im.save(final, 'png')
		final.seek(0)
		return final

	@commands.command(pass_context=True, aliases=['vaporwave', 'vape', 'vapewave'])
	async def vw(self, ctx, url:str, *, txt:str=None):
		"""Vaporwave an image!"""
		get_images = await self.get_images(ctx, urls=url, limit=1)
		if not get_images:
			return
		for url in get_images:
			if txt is None:
				txt = "vapor wave"
			b = await self.bytes_download(url)
			final = await self.bot.loop.run_in_executor(None, self.do_vw, b, txt)
			await self.bot.send_file(ctx.message.channel, final, filename='vapewave.png')

	@commands.command(pass_context=True)
	async def jagroshisgay(self, ctx, *, txt:str):
		x = await self.bot.send_message(ctx.message.channel, txt, replace_mentions=True)
		txt = u"\u202E " + txt
		await self.bot.edit_message(x, txt)

	@commands.command(pass_context=True, aliases=['achievement', 'ach'])
	async def mc(self, ctx, *, txt:str):
		"""Generate a Minecraft Achievement"""
		api = "https://mcgen.herokuapp.com/a.php?i=1&h=Achievement-{0}&t={1}".format(ctx.message.author.name, txt)
		b = await self.bytes_download(api)
		i = 0
		while sys.getsizeof(b) == 88 and i != 10:
			b = await self.bytes_download(api)
			if sys.getsizeof(b) != 0:
				i = 10
			else:
				i += 1
		if i == 10 and sys.getsizeof(b) == 88:
			await ctx.send("Minecraft Achievement Generator API is bad, pls try again")
			return
		await self.bot.upload(b, filename='achievement.png')

	@commands.command(aliases=['cow'])
	async def cowsay(self, *, txt:str):
		try:
			msg = await self.bot.run_process(["cowsay", txt], True)
			msg = msg
			await ctx.send("```\n"+msg+"```")
		except Exception as e:
			print(e)

	@commands.command(aliases=['dragon'])
	async def dragonsay(self, *, txt:str):
		msg = await self.bot.run_process(["cowsay", '-f', 'dragon', txt], True)
		msg = msg
		await ctx.send("```\n"+msg+"```")

	@commands.command(aliases=['sheep'])
	async def sheepsay(self, *, txt:str):
		msg = await self.bot.run_process(["cowsay", '-f', 'sheep', txt], True)
		msg = msg
		await ctx.send("```\n"+msg+"```")

	@commands.command(aliases=['dino'])
	async def dinosay(self, *, txt:str):
		msg = await self.bot.run_process(["cowsay", '-f', 'stegosaurus', txt], True)
		msg = msg
		await ctx.send("```\n"+msg+"```")

	@commands.command(aliases=['pony'])
	async def ponysay(self, *, txt:str):
		msg = await self.bot.run_process(["cowsay", '-f', 'unipony-smaller', txt], True)
		msg = msg
		await ctx.send("```\n"+msg+"```")

	@commands.command(aliases=['mech'])
	async def mechsay(self, *, txt:str):
		msg = await self.bot.run_process(["cowsay", '-f', 'mech-and-cow', txt], True)
		msg = msg
		await ctx.send("```\n"+msg+"```")

	@commands.command(aliases=['dragoncow', 'dragonandcow'])
	async def dragoncowsay(self, *, txt:str):
		msg = await self.bot.run_process(["cowsay", '-f', 'dragon-and-cow', txt], True)
		msg = msg
		await ctx.send("```\n"+msg+"```")

	# thanks RoadCrosser#3657
	@commands.group(pass_context=True, aliases=['eye'], invoke_without_command=True)
	async def eyes(self, ctx, url:str=None, eye:str=None, resize:str=None):
		get_images = await self.get_images(ctx, urls=url, limit=5)
		if not get_images:
			return
		for url in get_images:
			resize_amount = None
			monocle = False
			flipped = False
			flipped_count = 1
			if eye != None:
				eye = eye.lower()
			if eye is None or eye == 'default' or eye == '0':
				eye_location = self.files_path('eye.png')
			elif eye == 'spongebob' or eye == 'blue' or eye == '1':
				eye_location = self.files_path('spongebob_eye.png')
			elif eye == 'big' or eye == '2':
				eye_location = self.files_path('big_eye.png')
				resize_amount = 110
			elif eye == 'small' or eye == '3':
				eye_location = self.files_path('small_eye.png')
				resize_amount = 110
			elif eye == 'money' or eye == '4':
				eye_location = self.files_path('money_eye.png')
			elif eye == 'blood' or eye == 'bloodshot' or eye == '5':
				eye_location = self.files_path('bloodshot_eye.png')
				resize_amount = 200
			elif eye == 'red' or eye == '6':
				eye_location = self.files_path('red_eye.png')
				resize_amount = 200
			elif eye == 'meme' or eye == 'illuminati' or eye == 'triangle' or eye == '7':
				eye_location = self.files_path('illuminati_eye.png')
				resize_amount = 150
			elif eye == 'googly' or eye == 'googlyeye' or eye == 'plastic' or eye == '8':
				eye_location = self.files_path('googly_eye.png')
				resize_amount = 200
			elif eye == 'monocle' or eye == 'fancy' or eye == '9':
				eye_location = self.files_path('monocle_eye.png')
				resize_amount = 80
				monocle = True
			elif eye == 'flip' or eye == 'flipped' or eye == 'reverse' or eye == 'reversed' or eye == '10':
				eye_location = self.files_path('eye.png')
				eye_flipped_location = self.files_path('eye_flipped.png')
				flipped = True
			elif 'eyesCenter' in eye or eye == 'one' or eye == 'center' or eye == '11':
				eye_location = self.files_path('one_eye_center.png')
			else:
				eye_location = self.files_path('eye.png')
			if resize_amount is None:
				resize_amount = 130
			try:
				if resize != None:
					sigh = str(resize).split('.')
					if len(sigh) == 1:
						resize = int(resize)
					else:
						resize = float(resize)
					if resize == 0:
						resize_amount = 120
					else:
						resize_amount = resize*100
			except ValueError:
				resize_amount = 120
			x = await self.bot.send_message(ctx.message.channel, "ok, processing")
			b = await self.bytes_download(url)
			if b is False:
				if len(get_images) == 1:
					await ctx.send(':warning: **Command download function failed...**')
					return
				continue
			img = PIL.Image.open(b).convert("RGBA")
			eyes = PIL.Image.open(eye_location).convert("RGBA")
			data = {"url": url}
			headers = {"Content-Type":"application/json","Ocp-Apim-Subscription-Key": '3bb232c5dcba448c8b1e95da94b286cd'}
			async with aiohttp.ClientSession() as session:
				async with session.post('https://api.projectoxford.ai/face/v1.0/detect?returnFaceId=false&returnFaceLandmarks=true&returnFaceAttributes=headPose', headers=headers, data=json.dumps(data)) as r:
					faces = await r.json()
			if "error" in faces:
				await ctx.send(":warning: `Error occured in the API, could not process image url`")
				await self.bot.delete_message(x)
				return
			if len(faces) == 0:
				await ctx.send(":no_entry: `Face not detected`")
				await self.bot.delete_message(x)
				return
			eye_list = []
			for f in faces:
				if monocle == True:
					eye_list += ([((f['faceLandmarks']['pupilRight']['x'],f['faceLandmarks']['pupilRight']['y']),f['faceRectangle']['height'],(f['faceAttributes']['headPose']))])
				else:
					eye_list += (((f['faceLandmarks']['pupilLeft']['x'],f['faceLandmarks']['pupilLeft']['y']),f['faceRectangle']['height'],(f['faceAttributes']['headPose'])),((f['faceLandmarks']['pupilRight']['x'],f['faceLandmarks']['pupilRight']['y']),f['faceRectangle']['height'],(f['faceAttributes']['headPose'])))
			for e in eye_list:
				width, height = eyes.size
				h = e[1]/resize_amount*50
				width = h/height*width
				if flipped:
					if (flipped_count % 2 == 0):
						s_image = wand.image.Image(filename=eye_flipped_location)
					else:
						s_image = wand.image.Image(filename=eye_location)
					flipped_count += 1
				else:
					s_image = wand.image.Image(filename=eye_location)
				i = s_image.clone()
				i.resize(int(width), int(h))
				s_image = BytesIO()
				i.save(file=s_image)
				s_image.seek(0)
				inst = PIL.Image.open(s_image)
				yaw = e[2]['yaw']
				pitch = e[2]['pitch']
				width, height = inst.size
				pyaw = int(yaw/180*height)
				ppitch = int(pitch/180*width)
				new = PIL.Image.new('RGBA', (width+posnum(ppitch)*2, height+posnum(pyaw)*2), (255, 255, 255, 0))
				new.paste(inst, (posnum(ppitch), posnum(pyaw)))
				width, height = new.size
				coeffs = find_coeffs([(0, 0), (width, 0), (width, height), (0, height)], [(ppitch, pyaw), (width-ppitch, -pyaw), (width+ppitch, height+pyaw), (-ppitch, height-pyaw)])
				inst = new.transform((width, height), PIL.Image.PERSPECTIVE, coeffs, PIL.Image.BICUBIC).rotate(-e[2]['roll'], expand=1, resample=PIL.Image.BILINEAR)
				eyel = PIL.Image.new('RGBA', img.size, (255, 255, 255, 0))
				width, height = inst.size
				if monocle:
					eyel.paste(inst, (int(e[0][0]-width/2), int(e[0][1]-height/3.7)))
				else:
					eyel.paste(inst, (int(e[0][0]-width/2), int(e[0][1]-height/2)))
				img = PIL.Image.alpha_composite(img, eyel)
			final = BytesIO()
			img.save(final, "png")
			final.seek(0)
			await self.bot.upload(final, filename="eyes.png")
			await self.bot.delete_message(x)
		# except Exception as e:
		# 	exc_type, exc_obj, tb = sys.exc_info()
		# 	f = tb.tb_frame
		# 	lineno = tb.tb_lineno
		# 	filename = f.f_code.co_filename
		# 	linecache.checkcache(filename)
		# 	line = linecache.getline(filename, lineno, f.f_globals)
		# 	await ctx.send(code.format('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)))
		# 	os.remove(location)
		# 	os.remove(final_location)
		# 	os.remove(s_image_loc)

	@eyes.command(name='list', pass_context=True, invoke_without_command=True)
	async def eyes_list(self, ctx):
		eyes = ['Default - 0', 'Spongebob - 1', 'Big - 2', 'Small - 3', 'Money - 4', 'Bloodshot - 5', 'Red - 6', 'Illuminati - 7', 'Googly - 8', 'Monocle - 9', 'Flipped - 10', 'Center - 11']
		thing = []
		for s in eyes:
			thing.append('`'+s+'`')
		await ctx.send("In order to use, you must do `eyes image_url eye_type (name or number)`\n**Eye types**\n"+', '.join(thing))

	@commands.command(pass_context=True, aliases=['identify', 'captcha', 'whatis'])
	async def i(self, ctx, *, url:str):
		"""Identify an image/gif using Microsofts Captionbot API"""
		with aiohttp.ClientSession() as session:
			async with session.post("https://www.captionbot.ai/api/message", data={"conversationId": "FPrBPK2gAJj","waterMark": "","userMessage": url}) as r:
				pass
		load = await self.get_json("https://www.captionbot.ai/api/message?waterMark=&conversationId=FPrBPK2gAJj")
		msg = '`{0}`'.format(json.loads(load)['BotMessages'][-1])
		await ctx.send(msg)

#	@commands.command(pass_context=True, aliases=['mentionspam'])
#	async def ms(self, ctx, amount:int, id:str, channel:discord.Channel=None):
#		if amount > 100:
#			await ctx.send("2 many mentions asshole")
#			return
#		try:
#			await self.bot.delete_message(ctx.message)
#		except:
#			pass
#		user = discord.Server.get_member(ctx.message.server, id)
#		if user is None:
#			await ctx.send("invalid user id")
#			return
#		channels_readable = []
#		for s in ctx.message.server.channels:
#			if s.type == discord.ChannelType.voice:
#				continue
#			if user.permissions_in(s).read_messages and user.permissions_in(s).send_messages:
#				channels_readable.append(s)
#		count = 0
#		for i in range(amount):
#			if channel is None:
#				for s in channels_readable:
#					if count == amount:
#						break
#					x = await self.bot.send_message(s, '{0}'.format(user.mention))
#					await self.bot.delete_message(x)
#					count += 1
#					await asyncio.sleep(0.21)
#			else:
#				x = await self.bot.send_message(channel, '{0}'.format(user.mention))
#				await self.bot.delete_message(x)
#				await asyncio.sleep(0.21)
#		x = await ctx.send('done')
#		await asyncio.sleep(5)
#		await self.bot.delete_message(x)

	# yeah, hardcoded paths for life on this one
	@commands.group(pass_context=True, invoke_without_command=True, aliases=['texttospeech', 'text2speech'])
	async def tts(self, ctx, *, txt:str):
		"""Text to speech"""
		rand = self.bot.random()
		ogg_name = '{0}.ogg'.format(rand)
		path = '/var/www/vhosts/mods.nyc/bot.mods.nyc/ogg_files/{0}'.format(ogg_name)
		html = '<audio controls autoplay><source src="https://bot.facepunch.org/ogg_files/{0}" type="audio/ogg"></audio>'.format(ogg_name)
		html_file_name = '{0}.html'.format(rand)
		html_file = '/var/www/vhosts/mods.nyc/bot.mods.nyc/tts/{0}'.format(html_file_name)
		with open(html_file, 'wb') as f:
			f.write(html.encode())
			f.close()
		url_msg = 'https://bot.facepunch.org/tts/{0}'.format(html_file_name)
		url = 'https://text-to-speech-demo.mybluemix.net/api/synthesize?voice=en-US_AllisonVoice&X-WDC-PL-OPT-OUT=1&self.download=true&text={0}'.format(quote(txt))
		await self.download(url, path)
		await ctx.send(url_msg)

	@tts.command(name='custom', pass_context=True, invoke_without_command=True, aliases=['texttospeech', 'text2speech'])
	async def tts_custom(self, ctx, voice:str, *, txt:str):
		"""Text to speech"""
		voice = voice.lower()
		vv = None
		if voice == 'allison':
			vv = 'en-US_AllisonVoice'
		elif voice == 'michael':
			vv = 'en-US_MichaelVoice'
		elif voice == 'lisa':
			vv = 'en-US_LisaVoice'
		elif voice == 'kate':
			vv = 'en-GB_KateVoice'
		elif voice == 'renee':
			vv = 'fr-FR_ReneeVoice'
		elif voice == 'birgit':
			vv = 'de-DE_BirgitVoice'
		elif voice == 'dieter':
			vv = 'de-DE_DieterVoice'
		elif voice == 'francesca':
			vv = 'it-IT_FrancescaVoice'
		elif voice == 'emi':
			vv = 'ja-JP_EmiVoice'
		elif voice == 'isabela':
			vv = 'pt-BR_IsabelaVoice'
		elif voice == 'enrique':
			vv = 'es-ES_EnriqueVoice'
		elif voice == 'laura':
			vv = 'es-ES_LauraVoice'
		elif voice == 'sofia':
			vv = 'es-US_SofiaVoice'
		if vv is None:
			await ctx.send("**Invalid Voice**\nHere's a list of voices you can use `format: tts custom <voice (without location)> <text>`\n"+', '.join(self.voice_list))
			return
		rand = self.bot.random()
		ogg_name = 'tts_{0}.ogg'.format(rand)
		path = '/var/www/vhosts/mods.nyc/bot.mods.nyc/ogg_files/{0}'.format(ogg_name)
		html = '<audio controls autoplay><source src="https://bot.facepunch.org/ogg_files/{0}" type="audio/ogg"></audio>'.format(ogg_name)
		html_file_name = '{0}.html'.format(rand)
		html_file = '/var/www/vhosts/mods.nyc/bot.mods.nyc/tts/{0}'.format(html_file_name)
		with open(html_file, 'wb') as f:
			f.write(html.encode())
			f.close()
		url_msg = 'https://bot.facepunch.org/tts/{0}'.format(html_file_name)
		url = 'https://text-to-speech-demo.mybluemix.net/api/synthesize?voice={1}&text={0}&X-WDC-PL-OPT-OUT=1&self.download=true'.format(txt.replace(' ', '%20'), vv)
		await self.download(url, path)
		await ctx.send(url_msg)

	@tts.command(name='list', invoke_without_command=True)
	async def tts_list(self):
		await ctx.send("**List of custom voices**\nFormat: `tts custom <voice (without location)> <text>`\n"+', '.join(self.voice_list))

	@commands.command(pass_context=True, aliases=['wm'])
	async def watermark(self, ctx, url:str, mark:str=None):
		try:
			check = await self.isimage(url)
			if check == False:
				await ctx.send("Invalid or Non-Image!")
				return
			b = await self.bytes_download(url)
			if mark == 'brazzers' or mark is None:
				wmm = self.files_path('brazzers.png')
			else:
				check = await self.isimage(mark)
				if check == False:
					await ctx.send("Invalid or Non-Image for Watermark!")
					return
				wmm = await self.bytes_download(mark)
			final = BytesIO()
			with wand.image.Image(file=b) as img:
				if mark:
					with wand.image.Image(file=wmm) as wm:
						img.watermark(image=wm, left=int(img.width/15), top=int(img.height/10))
				else:
					with wand.image.Image(filename=wmm) as wm:
						img.watermark(image=wm, left=int(img.width/15), top=int(img.height/10))          
				img.save(file=final)
			final.seek(0)
			await self.bot.upload(final, filename='watermark.png')
		except Exception as e:
			exc_type, exc_obj, tb = sys.exc_info()
			f = tb.tb_frame
			lineno = tb.tb_lineno
			filename = f.f_code.co_filename
			linecache.checkcache(filename)
			line = linecache.getline(filename, lineno, f.f_globals)
			await ctx.send(code.format('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)))

	def do_glitch(self, b, amount, seed, iterations):
		b.seek(0)
		img = jpglitch.Jpeg(bytearray(b.getvalue()), amount, seed, iterations)
		final = BytesIO()
		img.save_image(final)
		final.seek(0)
		return final

	def do_gglitch(self, b):
		b = bytearray(b.getvalue())
		for x in range(0, sys.getsizeof(b)):
			if b[x] == 33:
				if b[x + 1] == 255:
					end = x
					break
				elif b[x + 1] == 249:
					end = x
					break
		for x in range(13, end):
			b[x] = random.randint(0, 255)
		return BytesIO(b)

	@commands.command(aliases=['jpglitch'], pass_context=True)
	async def glitch(self, ctx, url:str=None, iterations:int=None, amount:int=None, seed:int=None):
		try:
			if iterations is None:
				iterations = random.randint(1, 30)
			if amount is None:
				amount = random.randint(1, 20)
			elif amount > 99:
				amount = 99
			if seed is None:
				seed = random.randint(1, 20)
			get_images = await self.get_images(ctx, urls=url, msg=False)
			gif = False
			if not get_images:
				get_images = await self.get_images(ctx, urls=url, gif=True)
				if get_images:
					gif = True
				else:
					return
			for url in get_images:
				b = await self.bytes_download(url)
				if not gif:
					img = PIL.Image.open(b)
					b = BytesIO()
					img.save(b, format='JPEG')
					final = await self.bot.loop.run_in_executor(None, self.do_glitch, b, amount, seed, iterations)
					await self.bot.upload(final, filename='glitch.jpeg', content='Iterations: `{0}` | Amount: `{1}` | Seed: `{2}`'.format(iterations, amount, seed))
				else:
					final = await self.bot.loop.run_in_executor(None, self.do_gglitch, b)
					await self.bot.upload(final, filename='glitch.gif')
		except:
			await ctx.send("sorry, can't reglitch an image.")
			raise

	@commands.command(pass_context=True)
	async def glitch2(self, ctx, *urls:str):
		try:
			get_images = await self.get_images(ctx, urls=urls)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				await self.download(url, path)
				args = ['convert', '(', path, '-resize', '1024x1024>', ')', '-alpha', 'on', '(', '-clone', '0', '-channel', 'RGB', '-separate', '-channel', 'A', '-fx', '0', '-compose', 'CopyOpacity', '-composite', ')', '(', '-clone', '0', '-roll', '+5', '-channel', 'R', '-fx', '0', '-channel', 'A', '-evaluate', 'multiply', '.3', ')', '(', '-clone', '0', '-roll', '-5', '-channel', 'G', '-fx', '0', '-channel', 'A', '-evaluate', 'multiply', '.3', ')', '(', '-clone', '0', '-roll', '+0+5', '-channel', 'B', '-fx', '0', '-channel', 'A', '-evaluate', 'multiply', '.3', ')', '(', '-clone', '0', '-channel', 'A', '-fx', '0', ')', '-delete', '0', '-background', 'none', '-compose', 'SrcOver', '-layers', 'merge', '-rotate', '90', '-wave', '1x5', '-rotate', '-90', path]
				await self.bot.run_process(args)
				await self.bot.upload(path, filename='glitch2.png')
				os.remove(path)
		except:
			try:
				os.remove(path)
			except:
				pass
			raise

	def do_sort(self, image, interval, angle, randomness, s_func):
		input_img = PIL.Image.open(image)
		input_img.convert('RGBA')
		input_img.rotate(angle, expand=True)
		data = input_img.load()
		pixels = []
		for y in range(input_img.size[1]):
			pixels.append([])
			for x in range(input_img.size[0]):
				pixels[y].append(data[x, y])
		intervals = self.interval_functions[interval](pixels, image, angle)
		s_func = self.s_functions[s_func]
		sorted_pixels = pixelsort.sorter.sort_image(pixels, intervals, randomness, s_func)
		output_img = PIL.Image.new('RGBA', input_img.size)
		for y in range(output_img.size[1]):
			for x in range(output_img.size[0]):
				output_img.putpixel((x, y), sorted_pixels[y][x])
		if angle != 0:
			output_img.rotate(-angle, expand=True)
		output_img = pixelsort.util.crop_to(output_img, PIL.Image.open(image))
		b = BytesIO()
		output_img.save(b, 'png')
		b.seek(0)
		return b

	@commands.command(aliases=['pixelsort'], pass_context=True)
	async def sort(self, ctx, url:str=None, *args):
		try:
			angle = 0
			randomness = 0
			interval = 'edges'
			s_func = 'lightness'
			for arg in args:
				if arg.isdigit() and arg != '0' and angle is 0:
					angle = int(arg)
				elif randomness is 0 and arg.isdigit():
					randomness = int(arg)
				elif interval == 'edges':
					interval = str(arg)
				else:
					s_func = str(arg)
			if interval not in self.interval_functions.keys():
				await ctx.send(':warning: Invalid Interval Function.\nInterval Functions: `{0}`'.format(', '.join(list(self.interval_functions.keys()))))
				return
			elif s_func not in self.s_functions.keys():
				await ctx.send(':warning: Invalid Sorting Function.\nSorting Functions: `{0}`'.format(', '.join(list(self.s_functions.keys()))))
				return
			if angle >= 360:
				await ctx.send(':warning: Angle must be less then `360`.')
				angle = 0
			get_images = await self.get_images(ctx, urls=url)
			if not get_images:
				return
			for url in get_images:
				b = await self.bytes_download(url)
				if b is False:
					if len(get_images) == 1:
						await ctx.send(':warning: **Command download function failed...**')
						return
					continue
				img = await self.bot.loop.run_in_executor(None, self.do_sort, b, interval, angle, randomness, s_func)
				await self.bot.upload(img, filename='pixelsort.png', content='Interval: `{0}` | Sorting: `{1}`{2}{3}'.format(interval, s_func, ' | Angle: **{0}**'.format(angle) if angle != 0 else '', ' | Randomness: **{0}**'.format(randomness) if randomness != 0 else ''))
		except Exception as e:
			exc_type, exc_obj, tb = sys.exc_info()
			f = tb.tb_frame
			lineno = tb.tb_lineno
			filename = f.f_code.co_filename
			linecache.checkcache(filename)
			line = linecache.getline(filename, lineno, f.f_globals)
			await ctx.send(code.format('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)))

	@commands.command()
	async def bean(self, url:str):
		"""You got BEANED"""
		try:
			check = await self.isimage(url)
			if check is False:
				await ctx.send('Invalid or Non-Image!')
				return
			b = await self.bytes_download(url)
			bean_path = self.files_path('bean.png')
			bean = PIL.Image.open(bean_path)
			img = PIL.Image.open(b)
			width, height = bean.size
			bean.resize((int(width/50), int(height/50)))
			img.paste(bean, (math.floor(width/2), math.floor(height/2)))
			final = BytesIO()
			img.save(final, 'png')
			final.seek(0)
			await self.bot.upload(final, filename='beaned.png')
		except Exception as e:
			await ctx.send(e)

	@commands.command(aliases=['pixel'], pass_context=True)
	async def pixelate(self, ctx, *urls):
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=6, scale=3000)
			if not get_images:
				return
			img_urls = get_images[0]
			pixels = get_images[1]
			if pixels is None:
				pixels = 9
			scale_msg = get_images[2]
			if scale_msg is None:
				scale_msg = ''
			for url in img_urls:
				b = await self.bytes_download(url)
				if b is False:
					if len(img_urls) > 1:
						await ctx.send(':warning: **Command download function failed...**')
						return
					continue
				bg = (0, 0, 0)
				img = PIL.Image.open(b)
				img = img.resize((int(img.size[0]/pixels), int(img.size[1]/pixels)), PIL.Image.NEAREST)
				img = img.resize((int(img.size[0]*pixels), int(img.size[1]*pixels)), PIL.Image.NEAREST)
				load = img.load()
				for i in range(0, img.size[0], pixels):
					for j in range(0, img.size[1], pixels):
						for r in range(pixels):
							load[i+r, j] = bg
							load[i, j+r] = bg
				final = BytesIO()
				img.save(final, 'png')
				final.seek(0)
				await self.bot.upload(final, filename='pixelated.png', content=scale_msg)
				await asyncio.sleep(0.21)
		except:
			await ctx.send(':warning: `Too many pixels.`')

	async def do_retro(self, text, bcg):
		if '|' not in text:
			if len(text) >= 15:
				text = [text[i:i + 15] for i in range(0, len(text), 15)]
			else:
				split = text.split()
				if len(split) == 1:
					text = [x for x in text]
					if len(text) == 4:
						text[2] = text[2]+text[-1]
						del text[3]
				else:
					text = split
		else:
			text = text.split('|')
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:43.0) Gecko/20100101 Firefox/43.0'}
		payload = aiohttp.FormData()
		payload.add_field('current-category', 'all_effects')
		payload.add_field('bcg', bcg)
		payload.add_field('txt', '4')
		count = 1
		for s in text:
			if count > 3:
				break
			payload.add_field('text'+str(count), s.replace("'", "\'"))
			count += 1
		try:
			with aiohttp.ClientSession() as session:
				with aiohttp.Timeout(5):
					async with session.post('https://photofunia.com/effects/retro-wave?server=3', data=payload, headers=headers) as r:
						txt = await r.text()
		except asyncio.TimeoutError:
			return
		match = self.retro_regex.findall(txt)
		if match:
			download_url = match[0][0]
			b = await self.bytes_download(download_url)
			return b
		return False

	@commands.command()
	async def retro(self, *, text:str):
		retro_result = await self.do_retro(text, '5')
		if retro_result is False:
			await ctx.send(':warning: This text contains unsupported characters')
		else:
			await self.bot.upload(retro_result, filename='retro.png')

	@commands.command()
	async def retro2(self, *, text:str):
		retro_result = await self.do_retro(text, '2')
		if retro_result is False:
			await ctx.send(':warning: This text contains unsupported characters')
		else:
			await self.bot.upload(retro_result, filename='retro.png')

	@commands.command()
	async def retro3(self, *, text:str):
		retro_result = await self.do_retro(text, '4')
		if retro_result is False:
			await ctx.send(':warning: This text contains unsupported characters')
		else:
			await self.bot.upload(retro_result, filename='retro.png')

	def do_waaw(self, b):
		f = BytesIO()
		f2 = BytesIO()
		with wand.image.Image(file=b, format='png') as img:
			h1 = img.clone()
			width = int(img.width/2) if int(img.width/2) > 0 else 1
			h1.crop(width=width, height=int(img.height), gravity='east')
			h2 = h1.clone()
			h1.rotate(degree=180)
			h1.flip()
			h1.save(file=f)
			h2.save(file=f2)
		f.seek(0)
		f2.seek(0)
		list_im = [f2, f]
		imgs = [PIL.ImageOps.mirror(PIL.Image.open(i).convert('RGBA')) for i in list_im]
		min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
		imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
		imgs_comb = PIL.Image.fromarray(imgs_comb)
		final = BytesIO()
		imgs_comb.save(final, 'png')
		final.seek(0)
		return final

	#Thanks to Iguniisu#9746 for the idea
	@commands.command(pass_context=True, aliases=['magik3', 'mirror'])
	async def waaw(self, ctx, *urls:str):
		get_images = await self.get_images(ctx, urls=urls, limit=5)
		if not get_images:
			return
		for url in get_images:
			b = await self.bytes_download(url)
			if b is False:
				if len(get_images) == 1:
					await ctx.send(':warning: **Command download function failed...**')
					return
				continue
			final = await self.bot.loop.run_in_executor(None, self.do_waaw, b)
			await self.bot.upload(final, filename='waaw.png')

	def do_haah(self, b):
		f = BytesIO()
		f2 = BytesIO()
		with wand.image.Image(file=b, format='png') as img:
			h1 = img.clone()
			h1.transform('50%x100%')
			h2 = h1.clone()
			h2.rotate(degree=180)
			h2.flip()
			h1.save(file=f)
			h2.save(file=f2)
		f.seek(0)
		f2.seek(0)
		list_im = [f2, f]
		imgs = [PIL.ImageOps.mirror(PIL.Image.open(i).convert('RGBA')) for i in list_im]
		min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
		imgs_comb = np.hstack((np.asarray(i.resize(min_shape)) for i in imgs))
		imgs_comb = PIL.Image.fromarray(imgs_comb)
		final = BytesIO()
		imgs_comb.save(final, 'png')
		final.seek(0)
		return final

	@commands.command(pass_context=True, aliases=['magik4', 'mirror2'])
	async def haah(self, ctx, *urls:str):
		get_images = await self.get_images(ctx, urls=urls, limit=5)
		if not get_images:
			return
		for url in get_images:
			b = await self.bytes_download(url)
			if b is False:
				if len(get_images) == 1:
					await ctx.send(':warning: **Command download function failed...**')
					return
				continue
			final = await self.bot.loop.run_in_executor(None, self.do_haah, b)
			await self.bot.upload(final, filename='haah.png')

	def do_woow(self, b):
		f = BytesIO()
		f2 = BytesIO()
		with wand.image.Image(file=b, format='png') as img:
			h1 = img.clone()
			width = int(img.width) if int(img.width) > 0 else 1
			h1.crop(width=width, height=int(img.height/2), gravity='north')
			h2 = h1.clone()
			h2.rotate(degree=180)
			h2.flop()
			h1.save(file=f)
			h2.save(file=f2)
		f.seek(0)
		f2.seek(0)
		list_im = [f, f2]
		imgs = [PIL.Image.open(i).convert('RGBA') for i in list_im]
		min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
		imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
		imgs_comb = PIL.Image.fromarray(imgs_comb)
		final = BytesIO()
		imgs_comb.save(final, 'png')
		final.seek(0)
		return final

	@commands.command(pass_context=True, aliases=['magik5', 'mirror3'])
	async def woow(self, ctx, *urls:str):
		get_images = await self.get_images(ctx, urls=urls, limit=5)
		if not get_images:
			return
		for url in get_images:
			b = await self.bytes_download(url)
			if b is False:
				if len(get_images) == 1:
					await ctx.send(':warning: **Command download function failed...**')
					return
				continue
			final = await self.bot.loop.run_in_executor(None, self.do_woow, b)
			await self.bot.upload(final, filename='woow.png')

	def do_hooh(self, b):
		f = BytesIO()
		f2 = BytesIO()
		with wand.image.Image(file=b, format='png') as img:
			h1 = img.clone()
			width = int(img.width) if int(img.width) > 0 else 1
			h1.crop(width=width, height=int(img.height/2), gravity='south')
			h2 = h1.clone()
			h1.rotate(degree=180)
			h2.flop()
			h1.save(file=f)
			h2.save(file=f2)
		f.seek(0)
		f2.seek(0)
		list_im = [f, f2]
		imgs = [PIL.Image.open(i).convert('RGBA') for i in list_im]
		min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
		imgs_comb = np.vstack((np.asarray(i.resize(min_shape)) for i in imgs))
		imgs_comb = PIL.Image.fromarray(imgs_comb)
		final = BytesIO()
		imgs_comb.save(final, 'png')
		final.seek(0)
		return final

	@commands.command(pass_context=True, aliases=['magik6', 'mirror4'])
	async def hooh(self, ctx, *urls:str):
		get_images = await self.get_images(ctx, urls=urls, limit=5)
		if not get_images:
			return
		for url in get_images:
			b = await self.bytes_download(url)
			if b is False:
				if len(get_images) == 1:
					await ctx.send(':warning: **Command download function failed...**')
					return
				continue
			final = await self.bot.loop.run_in_executor(None, self.do_hooh, b)
			await self.bot.upload(final, filename='hooh.png')

	@commands.command(pass_context=True)
	async def flip(self, ctx, *urls:str):
		get_images = await self.get_images(ctx, urls=urls, limit=5)
		if not get_images:
			return
		for url in get_images:		
			b = await self.bytes_download(url)
			img = PIL.Image.open(b)
			img = PIL.ImageOps.flip(img)
			final = BytesIO()
			img.save(final, 'png')
			final.seek(0)
			await self.bot.upload(final, filename='flip.png')

	@commands.command(pass_context=True)
	async def flop(self, ctx, *urls:str):
		get_images = await self.get_images(ctx, urls=urls, limit=5)
		if not get_images:
			return
		for url in get_images:		
			b = await self.bytes_download(url)
			img = PIL.Image.open(b)
			img = PIL.ImageOps.mirror(img)
			final = BytesIO()
			img.save(final, 'png')
			final.seek(0)
			await self.bot.upload(final, filename='flop.png')

	@commands.command(pass_context=True, aliases=['inverse', 'negate'])
	async def invert(self, ctx, url:str=None, *, txt:str=None):
		if not url.startswith('http'):
			if txt:
				txt = url + txt
			else:
				txt = url
			get_images = await self.get_images(ctx, urls=url, limit=1)
		else:
			get_images = await self.get_images(ctx, urls=url, limit=1)
		if not get_images:
			return
		for url in get_images:		
			b = await self.bytes_download(url)
			img = PIL.Image.open(b).convert('RGBA')
			img = PIL.ImageOps.invert(img)
			final = BytesIO()
			img.save(final, 'png')
			final.seek(0)
			await self.bot.upload(final, filename='flop.png')

	@commands.command(aliases=['indicator'])
	async def regional(self, *, txt:str):
		msg = ''
		for s in txt.lower():
			if s in self.regional_map:
				msg += u'​'+self.regional_map[s]
			else:
				msg += s
		await ctx.send(msg)

	@commands.command(pass_context=True)
	async def react(self, ctx, *, txt:str):
		msg = None
		channel = ctx.message.channel
		for c in ctx.message.channel_mentions:
			channel = c
			txt = txt.replace(c.mention, '')
		if not channel.is_private:
			perms = channel.permissions_for(ctx.message.server.me)
			if perms.add_reactions is False:
				await ctx.send(':no_entry: `Sorry, I do not have add_rections permission.`')
				return
		for s in txt.split():
			if s.isdigit():
				if len(s) > 10:
					msg = await self.bot.get_message(channel, s)
					txt = txt.replace(s, '')
					break
		if msg is None:
			msg = ctx.message
		count = 0
		icount = 0
		continue_count = 0
		added = []
		indexs = {}
		_x = False
		word_emotes = ['cool', 'ok', 'ng', 'up', 'new', 'ab', 'cl', 'sos', 'id']
		for split in txt.lower().split():
			if split in word_emotes and split not in added:
				indexs[txt.lower().rindex(split)] = [len(split), self.emojis[split]]
			match = self.emote_regex.match(split)
			if match:
				em = None
				for e in self.bot.get_all_emojis():
					if e.id == str(match.group('id')):
						em = e
						break
				if em:
					indexs[txt.lower().rindex(split)] = [len(split), em]
		for s in txt.lower():
			if len(added) > 20:
				break
			if s == ' ':
				continue
			if icount in indexs:
				i = indexs[icount]
				if i[1] in added:
					continue
				continue_count += i[0]
				await self.bot.add_reaction(msg, i[1])
				added.append(i[1])
				count += 1
			else:
				if icount == 0:
					icount += 1
			if continue_count != 0:
				icount += 1
				continue_count -= 1
				continue
			em = None
			if s not in added:
				if s in self.regional_map:
					em = self.regional_map[s]
				elif s in self.emojis:
					em = self.emojis[s]
				else:
					for e in self.emojis:
						if self.emojis[e] == s:
							em = self.emojis[e]
							break
					if em is None:
						if s == '?':
							em = self.emojis['question']
						elif s == '!':
							em = self.emojis['exclamation']
						elif s == '#':
							em = self.emojis['hash']
			else:
				if s == 'a' or s == 'b' or s == 'm':
					em = self.emojis[s]
				elif s == 'c':
					em = self.emojis['copyright']
				elif s == 'r':
					em = self.emojis['registered']
				elif s == 'o':
					em = self.emojis['o2']
				elif s == 'p':
					em = self.emojis['parking']
				elif s == 'i':
					em = self.emojis['information_source']
				elif s == 'l':
					if txt.lower().count('i') <= 1:
						em = self.regional_map['i']
				elif s == 'e':
					em = self.emojis['email']
				elif s == 'm':
					em = self.emojis['scorpius']
				elif s == 'o':
					em = self.emojis['zero']
				elif s == 'x':
					if _x:
						em = self.emojis['heavy_multiplication_x']
					else:
						em = self.emojis[s]
						_x = True
			if em:
				await self.bot.add_reaction(msg, em)
				added.append(s)
				count += 1
				await asyncio.sleep(0.21)
			icount += 1
		if count == 0:
			await ctx.send(':no_entry: Invalid Text.')
		else:
			x = await self.bot.send_message(ctx.message.channel, ':white_check_mark: Added `{0}` reactions.'.format(count))
			await asyncio.sleep(5)
			try:
				if msg != ctx.message:
					await self.bot.delete_messages([x, ctx.message])
				else:
					await self.bot.delete_message(x)
			except:
				pass

	@commands.command()
	async def webmd(self):
		"""Your personal online medical question assistant!"""
		if self.webmd_count >= len(self.webmd_responses):
			self.webmd_count = 0
		kek = self.webmd_responses[self.webmd_count]
		self.webmd_count += 1
		await ctx.send(':information_source: *According to WebMD*\n**{0}**...'.format(kek))

	@commands.command(pass_context=True)
	async def wasted(self, ctx, *urls:str):
		"""GTA5 Wasted Generator"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				await self.download(url, path)
				args = ['convert', path]
				img = PIL.Image.open(path)
				aspectRatio = img.height / img.width
				aspectRatio2 = img.width / img.height
				height = img.height
				width = img.width
				if img.width < 512:
					args.append('-resize')
					width = 512
					height = math.floor(aspectRatio * 512)
					args.append('512x{0}'.format(height))
				if img.height < 512:
					args.append('-resize')
					height = 512
					width = math.floor(aspectRatio2 * 512)
					args.append(str(width))
				if img.width > 1500:
					args.append('-resize')
					width = 1500
					height = math.floor(aspectRatio * 1500)
					args.append('1500x{0}'.format(height))
				if img.height > 1500:
					args.append('-resize')
					height = 1500
					width = math.floor(aspectRatio2 * 1500)
					args.append(str(width))
				args.extend(['-recolor', '.3 .1 .3 .3 .1 .3 .3 .1 .3', '-fill', 'rgba(0,0,0,0.5)'])
				signHeight = height * 0.2
				args.extend(['-draw', 'rectangle 0, {0}, {1}, {2}'.format(height / 2 - signHeight / 2, width, height / 2 + signHeight / 2)])
				args.extend([
					'-gravity', 'South',
					'-font', self.files_path('pricedown.ttf'),
					'-fill', 'rgb(200,30,30)',
					'-stroke', 'black',
					'-strokewidth', '3',
					'-weight', '300'
				])
				args.extend([
					'-pointsize', str(math.floor(signHeight * 0.8)), 
					'-draw', 'text 0,{0} "wasted"'.format(math.floor(height / 2 - signHeight * 0.45)),
				path])
				await self.bot.run_process(args)
				await self.bot.upload(path, filename='wasted.png')
				del img
				os.remove(path)
		except:
			try:
				os.remove(path)
			except:
				pass
			raise

	@commands.command(pass_context=True, aliases=['greentext', '>'])
	async def green(self, ctx, *, txt:str):
		try:
			self.bot.pruned_messages.append(ctx.message)
			await self.bot.delete_message(ctx.message)
		except:
			pass
		await ctx.send('```css\n>{0}\n```'.format(txt), replace_mentions=True)

	@commands.command(pass_context=True, aliases=['lsd', 'drugs', 'wew'])
	async def rainbow(self, ctx, *urls:str):
		"""Change images color matrix multiple times into a gif"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				path2 = path[:-3]+'gif'
				await self.download(url, path)
				args = ['convert']
				for c in self.color_combinations:
					args.extend([
						'(',
							path,
							'-resize', '256x256>',
							'-colorize', '{0},{1},{2}'.format(c[0], c[1], c[2]),
						')'
					])
				args.extend([
					'-delay', '2',
					'-set', 'delay', '2',
					'-loop', '0',
				path2])
				await self.bot.run_process(args)
				await self.bot.upload(path2, filename='rainbow.gif')
				os.remove(path)
				os.remove(path2)
		except:
			try:
				os.remove(path)
				os.remove(path2)
			except:
				pass
			raise

	@commands.command(pass_context=True, aliases=['waves'])
	async def wave(self, ctx, *urls:str):
		"""Wave image multiple times into a gif"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				path2 = path[:-3]+'gif'
				await self.download(url, path)
				args = ['convert', '(', path, '-resize', '256x256>', ')', '-alpha', 'on', 'canvas:none', '-background', 'none']
				amp = 5
				while amp < 20:
					args.extend([
						'(',
							'-clone', '0',
							'-wave', '-' + str(amp) + 'x15',
						')'
					])
					amp += 5
				amp = 20
				while amp >= 5:
					args.extend([
						'(',
							'-clone', '0',
							'-wave', '-' + str(amp) + 'x15',
						')'
					])
					amp -= 5
				args.extend([
					'-delay', '4',
					'-set', 'delay', '4',
					'-loop', '0',
				path2])
				await self.bot.run_process(args)
				await self.bot.upload(path2, filename='wave.gif')
				os.remove(path)
				os.remove(path2)
		except:
			try:
				os.remove(path)
				os.remove(path2)
			except:
				pass
			raise

	@commands.command(pass_context=True)
	async def wall(self, ctx, *urls:str):
		"""Image multiplied with curved perspective"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				await self.download(url, path)
				await self.bot.run_process(['convert', '(', path, '-resize', '128', ')', '-virtual-pixel', 'tile', '-mattecolor', 'none', '-background', 'none', '-resize', '512x512!', '-distort', 'Perspective', '0,0,57,42  0,128,63,130  128,0,140,60  128,128,140,140', path])
				await self.bot.upload(path, filename='wall.png')
				os.remove(path)
		except:
			try:
				os.remove(path)
			except:
				pass
			raise

	@commands.command(pass_context=True, aliases=['cappend', 'layers'])
	async def layer(self, ctx, *urls:str):
		"""Layers an image with its self"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				await self.download(url, path)
				args = ['convert', path]
				args.extend([
					'(',
						path,
						'-flop',
					')',
					'+append',
					'(',
						'(',
							path,
							'-flip',
						')',
						'(',
							path,
							'-flop',
							'-flip',
						')',
						'+append',
					')',
					'-append',
				path])
				await self.bot.run_process(args)
				await self.bot.upload(path, filename='layer.png')
				os.remove(path)
		except:
			try:
				os.remove(path)
			except:
				pass
			raise

	@commands.command(pass_context=True)
	async def rotate(self, ctx, *urls:str):
		"""Rotate image X degrees"""
		get_images = await self.get_images(ctx, urls=urls, limit=3, scale=360)
		if not get_images:
			return
		img_urls = get_images[0]
		scale = get_images[1] if get_images[1] else random.choice([90, 180, 50, 45, 270, 120, 80])
		for url in img_urls:
			b = await self.bytes_download(url)
			img = PIL.Image.open(b).convert('RGBA')
			img = img.rotate(int(scale))
			final = BytesIO()
			img.save(final, 'png')
			final.seek(0)
			await self.bot.upload(final, filename='rotate.png', content='Rotated: `{0}°`'.format(scale))

	@commands.command(pass_context=True)
	async def dice(self, ctx, *urls:str):
		"""Dice up an image"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				path2 = path[:-3]+'miff'
				await self.download(url, path)
				img = PIL.Image.open(path)
				width, height = img.size
				size = min(math.ceil(width * .1), math.ceil(height * .1))
				fragmentsW = math.ceil(width / size)
				fragmentsH = math.ceil(height / size)
				total = fragmentsW * fragmentsH
				args = ['convert', '-quiet', path, '-crop', '{0}x{0}'.format(size), path2]
				await self.bot.run_process(args)
				args = ['montage', '-background', 'none', '-tile', '{0}x{1}'.format(fragmentsW, fragmentsH), '-geometry', '+0+0']
				i = 0
				while i < total:
					rand = random.randint(-2, 2)
					args.extend([
						'(',
							'{0}[{1}]'.format(path2, i), '-rotate', str(rand * 90), 
						')'
					])
					i += 1
				args.append(path)
				await self.bot.run_process(args)
				await self.bot.upload(path, filename='dice.png')
				os.remove(path)
				os.remove(path2)
				del img
		except:
			try:
				os.remove(path)
				os.remove(path2)
			except:
				pass
			raise

	@commands.command(pass_context=True)
	async def scramble(self, ctx, *urls:str):
		"""Scramble image"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				path2 = path[:-3]+'miff'
				await self.download(url, path)
				img = PIL.Image.open(path)
				width, height = img.size
				size = min(math.ceil(width * .1), math.ceil(height * .1))
				fragmentsW = math.ceil(width / size)
				fragmentsH = math.ceil(height / size)
				total = fragmentsW * fragmentsH
				left = []
				i = 0
				while i < total:
					left.append(i)
					i += 1
				args = ['convert', '-quiet', path, '-crop', '{0}x{0}'.format(size), path2]
				await self.bot.run_process(args)
				args = ['montage', '-background', 'none', '-tile', '{0}x{1}'.format(fragmentsW, fragmentsH), '-geometry', '+0+0']
				i = 0
				while i < total:
					r = random.randint(0, len(left)-1)
					sli = left[r]
					left.pop(r)
					rand = random.randint(-2, 2)
					args.extend(['(', '{0}[{1}]'.format(path2, sli), '-rotate', str(rand * 90), ')'])
					i += 1
				args.append(path)
				await self.bot.run_process(args)
				await self.bot.upload(path, filename='scramble.png')
				os.remove(path)
				os.remove(path2)
				del img
		except:
			try:
				os.remove(path)
				os.remove(path2)
			except:
				pass
			raise

	@commands.command(pass_context=True)
	async def scramble2(self, ctx, *urls:str):
		"""Scramble image without rotation"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				path2 = path[:-3]+'miff'
				await self.download(url, path)
				img = PIL.Image.open(path)
				width, height = img.size
				size = min(math.ceil(width * .1), math.ceil(height * .1))
				fragmentsW = math.ceil(width / size)
				fragmentsH = math.ceil(height / size)
				total = fragmentsW * fragmentsH
				left = []
				i = 0
				while i < total:
					left.append(i)
					i += 1
				args = ['convert', '-quiet', path, '-crop', '{0}x{0}'.format(size), path2]
				await self.bot.run_process(args)
				args = ['montage', '-background', 'none', '-tile', '{0}x{1}'.format(fragmentsW, fragmentsH), '-geometry', '+0+0']
				i = 0
				while i < total:
					r = random.randint(0, len(left)-1)
					sli = left[r]
					left.pop(r)
					args.extend(['{0}[{1}]'.format(path2, sli)])
					i += 1
				args.append(path)
				await self.bot.run_process(args)
				await self.bot.upload(path, filename='scramble2.png')
				os.remove(path)
				os.remove(path2)
				del img
		except:
			try:
				os.remove(path)
				os.remove(path2)
			except:
				pass
			raise

	@commands.command(pass_context=True, aliases=['multi'])
	async def multiply(self, ctx, *urls:str):
		"""Rotate and shrink image multiple times on a large canvas"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				await self.download(url, path)
				img = PIL.Image.open(path)
				width, height = img.size
				size = min(math.ceil(width * .1), math.ceil(height * .1))
				fragmentsW = math.ceil(width / size)
				fragmentsH = math.ceil(height / size)
				total = fragmentsW * fragmentsH
				args = ['convert', '-quiet', path, '-crop', '{0}x{0}'.format(size), path]
				await self.bot.run_process(args)
				args = ['montage', '-background', 'none', '-tile', '{0}x{1}'.format(fragmentsW, fragmentsH), '-geometry', '+0+0']
				i = 0
				while i < total:
					rand = random.randint(-2, 2)
					args.extend([
						'(',
							'{0}[{1}]'.format(path, i), '-rotate', str(rand * 90), 
						')'
					])
					i += 1
				args.append(path)
				await self.bot.run_process(args)
				await self.bot.upload(path, filename='wtf.png')
				os.remove(path)
				del img
		except:
			try:
				os.remove(path)
			except:
				pass
			raise

	@commands.command(pass_context=True)
	async def shake(self, ctx, *urls:str):
		"""Generate a Triggered Gif for a User or Image"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				path2 = path[:-3]+'gif'
				await self.download(url, path)
				await self.bot.run_process(['convert',
					'canvas:none',
					'-size', '512x512!',
					'-resize', '512x512!',
					'-draw', 'image over -60,-60 640,640 "{0}"'.format(path),
					'(',
						'canvas:none',
						'-size', '512x512!',
						'-draw', 'image over -45,-50 640,640 "{0}"'.format(path),
					')',
					'(',
						'canvas:none',
						'-size', '512x512!',
						'-draw', 'image over -50,-45 640,640 "{0}"'.format(path),
					')',
					'(',
						'canvas:none',
						'-size', '512x512!',
						'-draw', 'image over -45,-65 640,640 "{0}"'.format(path),
					')',
					'-layers', 'Optimize',
					'-set', 'delay', '2',
				path2])
				await self.bot.upload(path2, filename='shake.gif')
				os.remove(path)
				os.remove(path2)
		except Exception as e:
			await ctx.send(e)
			try:
				os.remove(path)
				os.remove(path2)
			except:
				pass

	@commands.command(pass_context=True, aliases=['360', 'grotate'])
	async def spin(self, ctx, *urls:str):
		"""Make image into circular form and rotate it 360 into a gif"""
		try:
			get_images = await self.get_images(ctx, urls=urls, limit=3)
			if not get_images:
				return
			for url in get_images:
				path = self.files_path(self.bot.random(True))
				path2 = path[:3]+'gif'
				await self.download(url, path)
				args = ['convert', '-alpha', 'on', '(', path, '-scale', '256x256>', '-scale', '256x256<', ')', '(', '-size', '256x256', 'xc:none', '-fill', 'white', '-draw', 'circle 128,128 128,0', ')', '-compose', 'copyopacity', '-background', 'white']
				i = 0
				while i <= 340:
					args.extend(['(', '-clone', '0', '-rotate', str(i), '-crop', '256x256+0+0!', '-clone', '1', '-composite', ')'])
					i += 20
				args.extend(['-compose', 'srcover', '-delete', '0', '-delete', '0', '-delay', '5', '-set', 'delay', '5', '-set', 'dispose', 'None', path2])
				await self.bot.run_process(args)
				await self.bot.upload(path, filename='spin.gif')
				os.remove(path)
				os.remove(path2)
		except:
			try:
				os.remove(path)
				os.remove(path2)
			except:
				pass
			raise

def setup(bot):
	bot.add_cog(Fun2(bot))