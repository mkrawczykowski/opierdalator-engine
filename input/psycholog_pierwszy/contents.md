#color_palette
	$color_main_accent: #034AA6
	$color_secondary_accent: #D9910D
	$color_text: #272727
	$color_headings: #272727
	$color_borders: #f6f6f6
	$color_background: #f2f2f2
	$color_background_2: #ffffff
	$color_background_3: #ff0000
	
#typography
button
	size: 16
	line_height: 1.2
text
	size: 16
	line_height: 1.2
heading_1
	size: 48
	line_height: 1.4
	
#components
button
	padding_vertical: 10
	padding_horizontal: 20
	background_color: $color_secondary_accent
	border_radius: 10
	border_width: 0
	
section
	padding_vertical: 80
	background_color: $color_background
	
row
	max_width: 1200
	background_color: $color_background_2
	
column
	background_color: $color_background_3
	
#content
@@section
@@row 1/2 5%
@@column
@@heading_1: testowy heading, ale nieco dłuższy, żeby sprawdzić, czy się łamie
@@text: jakiś krótki tekst
@@button: przycisk
@@column
@@heading_1: testowy heading
@@text: jakiś krótki tekst
@@button: przycisk


@@section
@@row
@@column
@@heading_1: nagłowek drugiej sekcji
@@text: to jest drugi akapit
@@button: przycisk drugi
