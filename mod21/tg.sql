CREATE TRIGGER check_phone_format
BEFORE INSERT ON students
FOR EACH ROW
WHEN (NEW.phone NOT GLOB '+7(9??)-[0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
BEGIN
    SELECT RAISE(ABORT, 'Неверный формат номера телефона');
END;
