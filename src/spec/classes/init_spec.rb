require 'spec_helper'
describe 'rest' do
  context 'with default values for all parameters' do
    it { should contain_class('rest') }
  end
end
