from mini import Mini

def test_numbers():
	assert Mini().eval('') == []
	assert Mini().eval('32') == [32]
	assert Mini().eval('32 42') == [32, 42]

def test_variables():
	assert Mini({'a' : 50}).eval('a') == [50]
	assert Mini().eval('a = 2 \n a') == [2, 2]

def test_operators():
	assert Mini.eval('(42 + 3)') == [45]

def test_functions():
	assert Mini().eval('sum(10 20)') == [30]